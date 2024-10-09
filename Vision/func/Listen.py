import speech_recognition as sr
import threading

# Initialize recognizer
recogniser = sr.Recognizer()

# Set recognizer parameters for optimized performance
recogniser.energy_threshold = 300
recogniser.dynamic_energy_threshold = True
recogniser.dynamic_energy_adjustment_damping = 0.15
recogniser.dynamic_energy_ratio = 1.5
recogniser.pause_threshold = 0.8
recogniser.operation_timeout = None
recogniser.phrase_threshold = 0.3
recogniser.non_speaking_duration = 0.5


def listen():
    # Using microphone as the audio source
    with sr.Microphone() as source:
        print("Listening....")
        # Adjusting for ambient noise for 0.5 seconds to avoid long delays
        recogniser.adjust_for_ambient_noise(source, duration=0.5)

        # Listening to the source for up to 5 seconds of silence, and limiting speech to 5 seconds
        audio_data = recogniser.listen(source, timeout=5, phrase_time_limit=5)

        try:
            print("Recognising....")
            # Recognize speech using Google Web Speech API (requires internet)
            text = recogniser.recognize_google(audio_data)
            print(f"Speech recognised: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None


def run_recognition():
    recognised_text = listen()


# Running the recognition process in a separate thread
recognition_thread = threading.Thread(target=run_recognition)
recognition_thread.start()
