import random
import sys
import webbrowser
import pywhatkit as kit
import pyjokes
import wikipedia
from requests import get
import cv2
import pyttsx3
import speech_recognition as sr
import os
import smtplib
from functions.alarm import alarm
from functions.battery import charge
from functions.calculation import calculate
from functions.close_app import closeApplication
from functions.my_email import send_email
from functions.hide_unhide import hide_or_show_folder
from functions.how_to_do import how_to_do
from functions.image_capture import captureImage
from functions.instaprofile import insta
from functions.internet_speed import check_internet_speed
from functions.my_location import mylocation
from functions.news import news
from functions.openApp import openApplication
from functions.read_pdf import pdf_reader
from functions.screenshot import take_screenshot
from functions.set_alarm import setAlarm
from functions.switch_window import switchWindow
from functions.takeCommand import takeCommand
from functions.volume_control import process_volume_command
from functions.weather import weather
from functions.wish import wish
from functions.youtube_video import youtube_song

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
# engine.setProperty(rate, 150)

# Function for text-to-speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Main function to handle user commands
def Taskexecution():
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

        # Volume control
        elif "volume" in query:
            process_volume_command(query)

        # Wikipedia search
        elif "wikipedia" in query:
            speak("Searching Wikipedia .....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "temparature" in query:
            weather()

        elif "how to do" in query:
            how_to_do()

        elif "alarm" in query:
            alarm()

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

        # Battery
        elif "battery" in query or "charge" in query:
            charge()

        # Internet Speed
        elif "internet speed" in query:
            check_internet_speed()


        # Maths Calcution
        elif "calculate" in query:
            calculate();

        # Web browsing
        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")
        elif "open google" in query:
            speak("What should I search on Google?")
            cm = takeCommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={cm}")

        # Function to take a screenshot based on user command
        elif "take screenshot" in query or "take a screenshot" in query:
            take_screenshot()

        # My Location using Ip Address
        elif "where i am" in query:
            mylocation()

        # Main code for Instagram profile check and profile picture download
        elif "instagram profile" in query or "profile on instagram" in query:
            insta()

        # Messaging
        elif "send message" in query:
            kit.sendwhatmsg("+919701133665", "Project Test", 23, 3)

        # Song in Youtube
        elif "play song on youtube" in query:
            youtube_song()

        elif "read pdf" in query:
            pdf_reader()

        elif "hide files" in query:
            hide_or_show_folder()

        # Main code to handle email request
        elif "send email" in query:
            try:
                speak("Please tell me the recipient's email address.")
                to = input("Enter the recipient's email address: ")  # Ask for recipient's email
                speak("What do you want to send?")
                content = takeCommand().lower()  # Capture the email content
                send_email(to, content)  # Call sendEmail with recipient and content
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")

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


if __name__ == "__main__":
    Taskexecution()
