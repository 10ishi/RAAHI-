from ultralytics import YOLO
import cv2
import speech_recognition as sr
import threading

model = YOLO("yolo11n.pt")

stop_camera = False


def listen_for_camera_stop():
    global stop_camera

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Camera control: say 'stop camera' to close the camera.")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            while not stop_camera:
                try:
                    print("Listening for camera stop...")

                    audio = recognizer.listen(
                        source,
                        timeout=2,
                        phrase_time_limit=3
                    )

                    command = recognizer.recognize_google(audio).lower()

                    print("Camera command:", command)

                    if (
                        "stop camera" in command
                        or "close camera" in command
                        or "exit camera" in command
                        or "quit camera" in command
                        or command == "stop"
                    ):
                        print("🛑 Stopping camera...")
                        stop_camera = True
                        break

                except sr.WaitTimeoutError:
                    continue

                except sr.UnknownValueError:
                    continue

                except sr.RequestError:
                    print("Speech recognition service unavailable.")
                    break

    except Exception as e:
        print("Microphone error:", e)


def detect_objects():

    global stop_camera
    stop_camera = False

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Could not open camera.")
        return []

    detected_objects = set()

    # Start microphone listener
    voice_thread = threading.Thread(
        target=listen_for_camera_stop,
        daemon=True
    )

    voice_thread.start()

    print("\n📷 Camera started.")
    print("Say 'stop camera' to close it.")
    print("Or press ESC.\n")

    while not stop_camera:

        ret, frame = cap.read()

        if not ret:
            print("❌ Could not read camera frame.")
            break

        # YOLO detection
        results = model(
            frame,
            verbose=False,
            conf=0.6
        )

        # Collect detected objects
        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])

                object_name = model.names[class_id]

                detected_objects.add(object_name)

        # Display camera
        annotated_frame = results[0].plot()

        cv2.imshow(
            "Raahi - Object Detection",
            annotated_frame
        )

        # ESC also stops camera
        if cv2.waitKey(1) & 0xFF == 27:
            stop_camera = True
            break

    # Close camera
    cap.release()
    cv2.destroyAllWindows()

    print("📷 Camera stopped.")

    # Give microphone thread a moment to finish
    voice_thread.join(timeout=1)

    return list(detected_objects)


if __name__ == "__main__":

    detected = detect_objects()

    print("\nDetected Objects:")

    if detected:
        print(", ".join(detected))
    else:
        print("Nothing detected.")
