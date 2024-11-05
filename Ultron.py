import datetime
import random
import sys
import webbrowser
import pywhatkit
import kit
import wikipedia
from requests import get
import cv2
import pyttsx3
import speech_recognition as sr
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# Text to speech function
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Voice to text function
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening ....")
        r.pause_threshold = 0.5
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected within the time limit.")
            speak("I didn't hear anything. Please try again.")
            return "none"

    try:
        print("Recognizing ....")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")

    except sr.UnknownValueError:
        speak("I couldn't understand. Please speak clearly.")
        return "none"
    except Exception as e:
        speak("Say that again ....")
        return "none"
    return query

# To wish us
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Ultron Sir, Please tell me what can I do.")

# Function to capture image directly
def captureImage():
    cap = cv2.VideoCapture(0)  # Open the webcam
    if not cap.isOpened():
        speak("Could not open the camera.")
        return

    ret, frame = cap.read()  # Capture a frame
    if ret:
        img_path = f"captured_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"  # Create a unique file name with timestamp
        cv2.imwrite(img_path, frame)  # Save the captured image
        speak(f"Image captured and saved as {img_path}")
        print(f"Image saved as {img_path}")
    else:
        speak("Failed to capture image.")

    cap.release()  # Release the camera

# To send email
def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("usestoreme@gmail.com", "*chanducharan2030#")
    server.sendmail('usestoreme@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wish()
    while True:
        query = takeCommand().lower()

        if "open notepad" in query:
            npath = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(npath)

        elif "open movies" in query:
            spath = "C:\\Users\\srava\\Desktop\\Movies"
            os.startfile(spath)

        elif "open command prompt" in query:
            os.startfile("C:\\Windows\\system32\\cmd.exe")

        elif "capture image" in query:
            captureImage()  # Call the function to capture the image

        elif "open camera" in query:
            # If you still want to open the camera for live view, you can include this block
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                cv2.imshow('webcam', img)
                k = cv2.waitKey(1)
                if k == 27:  # ESC key to exit
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_dir = "C:\\Users\\srava\\Desktop\\Movies\\Music"
            songs = os.listdir(music_dir)
            if songs:
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))  # Play the selected song

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            speak("Searching Wikipedia .....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")

        elif "open google" in query:
            speak("What should I search on Google?")
            cm = takeCommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={cm}")

        elif "send message" in query:
            kit.sendwhatmsg("+919701133665", "Project Test", 23, 3)

        elif "play song on youtube" in query:
            speak("What song do you want to play on YouTube?")
            cm = takeCommand().lower()
            if cm == "none":
                speak("Playing the default song.")
                kit.playonyt("Naatu Naatu")
            else:
                speak(f"Playing {cm} on YouTube.")
                kit.playonyt(cm)

        elif "send email" in query:
            try:
                speak("What do you want to send?")
                content = takeCommand().lower()
                to = "chanducharan2030@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent.")
            except Exception as e:
                print(e)
                speak("Sorry, didn't send.")

        elif "no thanks" in query:
            speak("Thanks for using me sir, have a good day.")
            sys.exit()

        speak("Sir, have anything else to do?")
