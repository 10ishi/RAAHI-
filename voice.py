import speech_recognition as sr
import pyttsx3


# -----------------------------
# INITIALIZATION
# -----------------------------

recognizer = sr.Recognizer()


# -----------------------------
# TEXT TO SPEECH
# -----------------------------

def speak(text):
    print("Assistant:", text)

    # Create a new engine every time
    engine = pyttsx3.init()

    engine.setProperty("volume", 1.0)
    engine.setProperty("rate", 150)

    engine.say(text)
    engine.runAndWait()

    engine.stop()


# -----------------------------
# SPEECH TO TEXT
# -----------------------------

def listen():

    with sr.Microphone() as source:

        print("\nListening...")

        # Adjust microphone for background noise
        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        # Listen
        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print("You:", text)

        return text.lower()

    except sr.UnknownValueError:

        print("Sorry, I could not understand you.")

        return ""

    except sr.RequestError:

        print("Speech recognition service is unavailable.")

        return ""


# -----------------------------
# MAIN ASSISTANT
# -----------------------------

def main():

    speak(
        "Hello! I am your accessibility assistant. "
        "How can I help you?"
    )

    while True:

        command = listen()


        # -----------------------------
        # HELLO
        # -----------------------------

        if "hello" in command:

            speak(
                "Hello! How can I help you?"
            )


        # -----------------------------
        # CAMERA
        # -----------------------------

        elif "what do you see" in command:

            speak(
                "I can identify objects around you "
                "using the camera."
            )


        # -----------------------------
        # HELP
        # -----------------------------

        elif "help" in command:

            speak(
                "You can say hello, "
                "ask what do you see, "
                "or say stop to exit."
            )


        # -----------------------------
        # STOP
        # -----------------------------

        elif "stop" in command or "exit" in command:

            speak("Goodbye!")

            break


        # -----------------------------
        # NOTHING UNDERSTOOD
        # -----------------------------

        elif command == "":

            speak(
                "Sorry, I didn't understand."
            )


        # -----------------------------
        # UNKNOWN COMMAND
        # -----------------------------

        else:

            speak(
                "I heard you, but I don't understand "
                "that command yet."
            )


# -----------------------------
# START PROGRAM
# -----------------------------

if __name__ == "__main__":
    main()
