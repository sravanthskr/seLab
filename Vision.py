import webbrowser

import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random  # Import the random module
import requests
from requests import get
import wikipedia
import pywhatkit as kit
import smtplib as sm
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# 0 for male, 1 for female
engine.setProperty('voice', voices[0].id)

# Text to speech function
def speak(audio):
    print(audio)
    engine.say(audio)
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
        return query
    except sr.UnknownValueError:
        speak("I couldn't understand. Please speak clearly.")
        return "none"
    except Exception as e:
        speak("Say that again ....")
        return "none"

# To wish us
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Vision Sir, Please tell me what can I do.")

# to send email
def sendEmail(to, content):
    server=sm.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("usestoreme@gmail.com", "*chanducharan2030#")
    server.sendmail('chanducharan2030@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wish()
    while True: #is commented out for single execution
    #if True:  Replace this with `while True` for continuous execution
        query = takeCommand().lower()
        if "open notepad" in query:
            npath = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(npath)

        elif "open movies" in query:
            spath = "C:\\Users\\srava\\Desktop\\Movies"
            os.startfile(spath)

        elif "open command prompt" in query:
            os.startfile("C:\\Windows\\system32\\cmd.exe")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:  # ESC key to exit
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_dir = "C:\\Users\\srava\\Desktop\\Movies\\Music"
            songs = os.listdir(music_dir)
            if songs:
                song = random.choice(songs)  # Choose a random song
                os.startfile(os.path.join(music_dir, song))
            else:
                speak("No music files found in the directory.")

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(" Your Ip address is {ip} ")

        elif "wikipedia" in query:
            speak("Searching Wikipedia .....")
            query = query.replace("Wikipedia" , "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")

        elif "open google" in query:
            speak("What should i search on google")
            cm=takeCommand().lower()
            webbrowser.open(f"{cm}") # its opening anything inside that in browser

        elif "send message" in query:
            # hour and minutes is present time or the time to send in 24 hour format
            kit.sendwhatmsg("+919701133665" , "Project Test",23, 3)

        elif "play song on youtube" in query:
            #speak("What should i search on Youtube")
            #cm = takeCommand().lower()
            #kit.playonyt(f"{cm}")
            kit.playonyt(f"thangalayan")

        elif "email to charan" in query:
            try:
                speak("What do you want to send")
                content = takeCommand().lower()
                to = "chanducharan2030@gmail.com"
                sendEmail(to,content)
                speak("Email has sent")

            except Exception as e:
                print(e)
                speak("Sorry didnt send")

        elif "no thanks" in query:
            speak("Thanks for using me sir, have a good day")
            sys.exit()

        speak("Sir, have anything else to do")