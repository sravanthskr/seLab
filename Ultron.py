import datetime
import random
import sys
import webbrowser
import requests
import pyautogui
import pywhatkit as kit
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import winsound
import pyjokes
import wikipedia
from requests import get
import cv2
import pyttsx3
import speech_recognition as sr
import os
import smtplib

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function for text-to-speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Function to recognize voice commands
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

# Function to greet the user
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning")
    elif hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Ultron Sir, Please tell me what can I do.")

# Function to capture an image using webcam
def captureImage():
    cap = cv2.VideoCapture(0)  # Open the webcam
    if not cap.isOpened():
        speak("Could not open the camera.")
        return

    ret, frame = cap.read()
    if ret:
        img_path = f"captured_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(img_path, frame)
        speak(f"Image captured and saved as {img_path}")
        print(f"Image saved as {img_path}")
    else:
        speak("Failed to capture image.")
    cap.release()

# Function to switch windows with Alt+Tab
def switchWindow():
    speak("Switching the window.")
    pyautogui.keyDown("alt")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.keyUp("alt")

# Function to fetch and read out the latest news
def news():
    main_url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=d4c92e160722416ba2e1782022053c86'
    try:
        main_page = requests.get(main_url).json()
        articles = main_page.get("articles", [])
        day = ["first", "second", "third", "fourth", "fifth",
               "sixth", "seventh", "eighth", "ninth", "tenth"]
        head = []
        for i, ar in enumerate(articles[:10]):
            head.append(ar["title"])
        for i in range(len(head)):
            speak(f"Today's {day[i]} news is: {head[i]}")
    except requests.exceptions.RequestException as e:
        print("Error fetching news:", e)
        speak("Sorry, I couldn't retrieve the news at the moment.")

# Your email and password
email = "usestoreme@gmail.com"
password = "chanducharan2030"

# Function to send email
def sendEmail(to, content):
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to
        msg['Subject'] = "Automated Email"  # Add subject line if needed
        msg.attach(MIMEText(content, 'plain'))

        # Connect to the server and send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, to, text)
        server.quit()
        speak("Email has been sent.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")

# Function to open applications
def openApplication(app_name):
    app_paths = {
        "notepad": "C:\\Windows\\System32\\notepad.exe",
        "command prompt": "C:\\Windows\\system32\\cmd.exe",
        "movies": "C:\\Users\\srava\\Desktop\\Movies"
    }
    if app_name in app_paths:
        os.startfile(app_paths[app_name])
        speak(f"Opening {app_name}.")
    else:
        speak("Application not recognized.")

# Function to close applications
def closeApplication(app_name):
    app_processes = {
        "notepad": "notepad.exe",
        "command prompt": "cmd.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe"
    }
    if app_name in app_processes:
        os.system(f"taskkill /f /im {app_processes[app_name]}")
        speak(f"Closing {app_name}.")
    else:
        speak("Application not recognized.")

# Function to set an alarm
def setAlarm():
    speak("At what time should I set the alarm? Please specify in hour and minute.")
    alarm_time = takeCommand().lower()
    try:
        alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
        speak(f"Alarm set for {alarm_hour}:{alarm_minute}.")
        while True:
            now = datetime.datetime.now()
            if now.hour == alarm_hour and now.minute == alarm_minute:
                speak("Alarm is ringing!")
                winsound.Beep(1000, 10000)
                break
            time.sleep(30)
    except ValueError:
        speak("Please provide a valid time in HH:MM format.")

# Main function to handle user commands
if __name__ == "__main__":
    wish()
    while True:
        query = takeCommand().lower()

        # Opening applications
        if "open notepad" in query:
            openApplication("notepad")
        elif "open movies" in query:
            openApplication("movies")
        elif "open command prompt" in query:
            openApplication("command prompt")
        elif "capture image" in query:
            captureImage()
        elif "play music" in query:
            music_dir = "C:\\Users\\srava\\Desktop\\Movies\\Music"
            songs = os.listdir(music_dir)
            if songs:
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))

        # System information
        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        # Wikipedia search
        elif "wikipedia" in query:
            speak("Searching Wikipedia .....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Web browsing
        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")
        elif "open google" in query:
            speak("What should I search on Google?")
            cm = takeCommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={cm}")

        # Messaging and media functions
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

        # Main code to handle email request
        elif "send email" in query:
            try:
                speak("Please tell me the recipient's email address.")
                to = input("Enter the recipient's email address: ")  # Ask for recipient's email

                speak("What do you want to send?")
                content = takeCommand().lower()  # Capture the email content

                sendEmail(to, content)  # Call sendEmail with recipient and content
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")


        # Application control
        elif "close notepad" in query:
            closeApplication("notepad")

        # Alarm function
        elif "set alarm" in query:
            setAlarm()

        # Tell a joke
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        # Window switcher
        elif "switch the window" in query:
            switchWindow()

        # Latest news
        elif "tell me news" in query:
            speak("Please wait Sir, Getting Latest News")
            news()

        # System commands
        elif "shut down" in query:
            speak("Shutting down the system in 5 seconds.")
            os.system("shutdown /s /t 5")
        elif "restart" in query:
            speak("Restarting the system in 5 seconds.")
            os.system("shutdown /r /t 5")
        elif "sleep" in query:
            speak("Putting the system to sleep.")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        # Exit command
        elif "no thanks" in query:
            speak("Thank you for using me, have a good day!")
            sys.exit()

        speak("Sir, do you have any other commands?")
