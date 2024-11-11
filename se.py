import operator
import random
import sys
import datetime
import time
import smtplib
import webbrowser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pywhatkit as kit
import PyPDF2
import instaloader
import psutil
import pyjokes
import speedtest
import winsound
from pywikihow import search_wikihow
import cv2
import pyttsx3
import requests
import speech_recognition as sr
import os
import pyautogui
import re
from bs4 import BeautifulSoup
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import wikipedia
from requests import get

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

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning")
    elif hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am your Virtual Assistant, Please tell me what can I do.")


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


# Initialize audio interface for volume control
def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

# Set volume to a specific percentage
def set_volume(percent):
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(percent / 100, None)

# Process voice command to adjust volume
def process_volume_command(query):
    if "volume up" in query:
        pyautogui.press("volumeup")
    elif "volume down" in query:
        pyautogui.press("volumedown")
    elif "mute" in query:
        pyautogui.press("volumemute")
    elif "volume to" in query:
        try:
            percent = int(query.split("set volume to")[1].strip().replace("%", ""))
            if 0 <= percent <= 100:
                set_volume(percent)
                print(f"Volume set to {percent}%")
            else:
                print("Please specify a volume between 0 and 100.")
        except ValueError:
            print("Could not understand the volume level. Please try again.")

# Function to switch windows with Alt+Tab
def switchWindow():
    speak("Switching the window.")
    pyautogui.keyDown("alt")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.keyUp("alt")

def how_to_do():
    while True:
        speak("Please tell me what you want to know")
        how = takeCommand()
        try:
            if "exit" in how or "close" in how:
                break
            else:
                max_results = 1
                how_to = search_wikihow(how, max_results)
                assert len(how_to) == 1
                how_to[0].print()
                speak(how_to[0].summary)
        except Exception as e:
            speak("Sorry, I am not able to find this")


# Function to fetch the temperature for the city
def get_temperature(city_name):
    search = f"temperature in {city_name}"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(r.text, "html.parser")

    try:
        # Extract temperature
        temp = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
        speak(f"The current temperature in {city_name} is {temp}.")
    except AttributeError:
        speak(f"Sorry, I couldn't find the temperature information for {city_name}.")


# Function to extract the city name from the query
def extract_city_name(query):
    match = re.search(r"temperature in ([\w\s]+)", query, re.IGNORECASE)
    if match:
        return match.group(1).strip()  # Remove extra spaces if any
    return None

def take_screenshot():
    speak("Please tell me the name for this screenshot file.")
    name = takeCommand().lower()  # Get the name for the screenshot file

    speak("Please hold the screen for a few seconds, I am taking the screenshot.")
    time.sleep(3)  # Wait for 3 seconds before taking the screenshot

    # Take the screenshot
    img = pyautogui.screenshot()

    # Save the screenshot with the name provided by the user
    img.save(f"{name}.png")

    speak("I'm done, sir. The screenshot is saved in our main folder.")
    speak("Now, I am ready for your next command.")

def mylocation():
    speak("Wait sir, let me check.")
    try:
        # Get the public IP address
        ipAdd = requests.get('https://api.ipify.org').text
        print(f"IP Address: {ipAdd}")

        # Get the geographical details using the IP address
        url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
        geo_requests = requests.get(url)
        geo_data = geo_requests.json()

        # Extract city and country information
        city = geo_data['city']
        country = geo_data['country']

        # Respond with the location information
        speak(f"Sir, I am not sure, but I think we are in {city} city of {country} country.")

    except Exception as e:
        speak("Sorry sir, due to network issues, I am not able to find where we are.")
        print(f"Error: {e}")

def insta():
    speak("Sir, please enter the username correctly.")
    name = input("Enter username here: ")
    speak(f"Sir, here is the profile of the user {name}.")
    time.sleep(5)

    speak("Sir, would you like to download the profile picture of this account?")
    condition = takeCommand().lower()

    if "yes" in condition:
        mod = instaloader.Instaloader()  # Ensure you have installed the instaloader package
        mod.profile_pic_only = True  # Corrected from 'profile_pic_on1y' to 'profile_pic_only'

        # Download the profile picture
        mod.download_profile(name, profile_pic_only=True)

        speak("I'm done, sir. The profile picture is saved in our main folder.")
    else:
        pass


def youtube_song():
    speak("What song do you want to play on YouTube?")
    cm = takeCommand().lower()
    if cm == "none":
        speak("Playing the default song.")
        kit.playonyt("Naatu Naatu")
    else:
        speak(f"Playing {cm} on YouTube.")
        kit.playonyt(cm)


# Function to read PDF file
def pdf_reader():
    speak("Please tell me the name of the PDF file to read.")
    book_name = input("Please enter the name of the PDF file: ")  # User provides the name of the PDF file

    try:
        # Open the PDF file
        with open(book_name, 'rb') as book:
            pdfReader = PyPDF2.PdfFileReader(book)  # Read the PDF using PyPDF2
            pages = pdfReader.numPages  # Get the number of pages
            speak(f"Total number of pages in this book: {pages}")

            speak("Sir, please enter the page number I have to read.")
            pg = int(input("Please enter the page number: "))  # User provides the page number

            if pg < pages:
                page = pdfReader.getPage(pg)  # Get the specified page
                text = page.extractText()  # Extract text from the page
                speak(text)  # Read out the text to the user
            else:
                speak(f"Sorry sir, the page number {pg} is out of range. This book has only {pages} pages.")
    except FileNotFoundError:
        speak("Sorry, I couldn't find the file. Please make sure the file name is correct.")
    except Exception as e:
        speak(f"Sorry sir, an error occurred: {str(e)}")

def charge():
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"This device has {percentage} % battery")


def get_operator_fn(op):
    # Map operators to functions
    operators = {
        'plus': operator.add,
        'minus': operator.sub,
        'multiplied': operator.mul,
        'divided': operator.truediv
    }
    return operators.get(op)


def eval_binary_expr(op1, oper, op2):
    # Convert operands to integers and evaluate the expression
    op1, op2 = int(op1), int(op2)
    operator_fn = get_operator_fn(oper)
    return operator_fn(op1, op2)


def calculate():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Say what you want to calculate, for example: 3 plus 3")
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            # Recognize the user's speech
            my_string = r.recognize_google(audio)
            print(f"You said: {my_string}")

            # Split the input to extract operands and the operator
            expression = my_string.split()
            if len(expression) == 3:
                operand1, operator, operand2 = expression
                result = eval_binary_expr(operand1, operator, operand2)
                speak(f"Your result is {result}")
            else:
                speak("I couldn't understand the expression, please say it again.")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand the audio.")
        except sr.RequestError:
            speak("Sorry, there was an error with the speech service.")
        except Exception as e:
            speak(f"An error occurred: {e}")

# Command to hide the folder
def hide_or_show_folder(query):
    if "hide files" in query or "hide this folder" in query:
        speak("Sir, please tell me the folder path you want to hide.")
        folder_path = input("Enter folder path to hide: ")

        if os.path.exists(folder_path):
            # Hide the folder and files using attrib command
            os.system(f'attrib +h +s "{folder_path}" /s /d')
            speak(f"All files in the folder '{folder_path}' are now hidden.")
        else:
            speak("The folder path you provided does not exist.")

    # Command to make the folder visible to everyone
    elif "unhide for everyone" in query or "make it unhide" in query:
        speak("Sir, please tell me the folder path you want to make visible.")
        folder_path = input("Enter folder path to make visible: ")

        if os.path.exists(folder_path):
            # Make the folder and files visible
            os.system(f'attrib -h -s "{folder_path}" /s /d')
            speak(f"All files in the folder '{folder_path}' are now visible.")
        else:
            speak("The folder path you provided does not exist.")

    # If the user wants to leave it as is
    elif "leave it" in query or "leave for now" in query:
        speak("Ok sir, leaving the folder as it is.")

    else:
        speak("Sorry sir, I did not understand the command.")



# Main function to handle weather query
def weather(query):
    print(f"Query received: {query}")  # Debugging print statement
    city = extract_city_name(query)
    print(f"City extracted: {city}")  # Debugging print statement

    if city:
        get_temperature(city)  # Get the temperature for the city
    else:
        speak("Sorry, I couldn't understand the city name. Please mention the city clearly.")

def check_internet_speed():
    st = speedtest.Speedtest()
    dl = st.download() / 1_000_000  # Convert download speed to Mbps
    up = st.upload() / 1_000_000  # Convert upload speed to Mbps
    speak(f"Download speed is {dl:.2f} Mbps and Upload speed is {up:.2f} Mbps.")

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

def alarm():
    speak("Please tell the time to set Alarm. For example, say Set alarm to 6:30 AM")
    tt = takeCommand()

    # Clean and format the voice input to match time format for alarm function
    if "set alarm to" in tt.lower():
        tt = tt.replace("set alarm to ", "")
        tt = tt.replace(".", "")
        tt = tt.upper()  # Convert to uppercase for AM/PM consistency
        MyAlarm.alarm(tt)
    else:
        speak("I didn't catch the time. Please try again.")
def MyAlarm(Timing):
    # Parse the time given in the format "HH:MM AM/PM"
    altime = datetime.datetime.strptime(Timing, "%I:%M %p")
    Horeal = altime.hour
    Mireal = altime.minute

    print(f"Alarm is set for {Timing}")
    while True:
        # Get the current hour and minute
        current_time = datetime.datetime.now()
        if current_time.hour == Horeal and current_time.minute == Mireal:
            print("Alarm is ringing!")
            winsound.PlaySound('alarm_sound.wav', winsound.SND_LOOP)  # Replace 'alarm_sound.wav' with your own alarm sound
            break

def send_email(to, content):
    email = "usestoreme@gmail.com"
    password = "chanducharan2030"

    try:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to
        msg['Subject'] = "Automated Email"
        msg.attach(MIMEText(content, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, to, text)
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")

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

        # Wikipedia search
        elif "wikipedia" in query:
            speak("Searching Wikipedia .....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Volume control
        elif "volume" in query:
            process_volume_command(query)

        elif "temperature" in query:
            weather(query)

        elif "tell me info" in query:
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
            hide_or_show_folder(query)

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
