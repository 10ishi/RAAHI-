import speech_recognition as sr
import pyttsx3

from object_detection import detect_objects


# Speech recognizer
recognizer = sr.Recognizer()


# --------------------------------------------------
# SPEAK FUNCTION
# --------------------------------------------------

def speak(text):

    print("Raahi:", text)

    engine = pyttsx3.init()

    engine.setProperty("volume", 1.0)

    engine.setProperty("rate", 150)

    engine.say(text)

    engine.runAndWait()

    engine.stop()


# --------------------------------------------------
# LISTEN FUNCTION
# --------------------------------------------------

def listen():

    try:

        with sr.Microphone() as source:

            print("\n🎤 Listening...")

            # Adjust microphone for background noise
            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            # Listen to user
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )


        # Convert speech to text
        text = recognizer.recognize_google(audio)

        print("You:", text)

        return text.lower().strip()


    except sr.WaitTimeoutError:

        print("No speech detected.")

        return ""


    except sr.UnknownValueError:

        print("Sorry, I could not understand you.")

        return ""


    except sr.RequestError:

        print("Speech recognition service is unavailable.")

        return ""


# --------------------------------------------------
# OBJECT DETECTION COMMAND
# --------------------------------------------------

def start_camera():

    speak(
        "Let me check what is around you."
    )


    # Start camera
    objects = detect_objects()


    # Camera has now stopped
    speak(
        "The camera has stopped."
    )


    # Tell user what was detected
    if objects:

        object_list = ", ".join(objects)

        speak(
            "I detected " + object_list
        )

    else:

        speak(
            "I could not detect any objects."
        )


# --------------------------------------------------
# MAIN RAahi ASSISTANT
# --------------------------------------------------

def main():

    # Starting message
    speak(
        "Hello! I am Raahi, your accessibility assistant. "
        "How can I help you?"
    )


    while True:

        # Listen for command
        command = listen()


        # ------------------------------------------
        # CAMERA COMMAND
        # ------------------------------------------

        if (
            "what do you see" in command
            or "what can you see" in command
            or "what is in front of me" in command
            or "what is around me" in command
            or "look around" in command
            or "describe my surroundings" in command
            or "scan the room" in command
        ):

            start_camera()


        # ------------------------------------------
        # GREETING
        # ------------------------------------------

        elif (
            "hello" in command
            or "hi" in command
            or "hey" in command
        ):

            speak(
                "Hello! How can I help you?"
            )


        # ------------------------------------------
        # HELP
        # ------------------------------------------

        elif "help" in command:

            speak(
                "You can ask me what I see, "
                "say hello, or say stop to exit."
            )


        # ------------------------------------------
        # EXIT RAahi
        # ------------------------------------------

        elif (
            command == "stop"
            or command == "exit"
            or command == "quit"
            or command == "goodbye"
        ):

            speak(
                "Goodbye!"
            )

            break


        # ------------------------------------------
        # NOTHING UNDERSTOOD
        # ------------------------------------------

        elif command == "":

            speak(
                "Sorry, I didn't understand."
            )


        # ------------------------------------------
        # UNKNOWN COMMAND
        # ------------------------------------------

        else:

            speak(
                "I heard you, but I don't understand "
                "that command yet."
            )


# --------------------------------------------------
# PROGRAM START
# --------------------------------------------------

if __name__ == "__main__":

    main()
