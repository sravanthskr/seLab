import pyttsx3

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')

engine.setProperty('rate', 200)
engine.setProperty('voice', voices[0].id)

def Speak(*args, **kwargs):
    audio = ""
    for i in args:
        audio += str(i)
    print(audio)
    engine.say(audio)
    engine.runAndWait()