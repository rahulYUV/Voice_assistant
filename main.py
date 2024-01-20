import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
from bs4 import BeautifulSoup
from pywinauto.application import Application
import warnings
import pywhatkit


warnings.filterwarnings("ignore", category=UserWarning)



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=1 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am jarvis. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('rootrahul21@gmail.com', to, content)
    server.close()

if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()


        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            

        elif 'jarvis open my computer lab' in query:
            webbrowser.open("https://r.search.yahoo.com/_ylt=Awr1SUzoRoZkxUcDT0K7HAx.;_ylu=Y29sbwNzZzMEcG9zAzIEdnRpZAMEc2VjA3Ny/RV=2/RE=1686550376/RO=10/RU=https%3a%2f%2fironman.fandom.com%2fwiki%2fJ.A.R.V.I.S./RK=2/RS=G7XqSx1utiWOWdjy4yNa_XofjIA-")
            speak('welcome to your super computer lab tony stark sir ')
            speak('how are you sir')
            speak('your missile is ready')

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")



        elif 'play music' in query:
            music_dir = "D:\music"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "harry@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend harry. I am not able to send this email")

        elif 'what is the weather' in query:
            try:
                speak("Please tell me the city name")
                city_name = takeCommand().lower()
                url = f"https://www.google.com/search?q={city_name}&oq={city_name}&aqs=chrome.0.35i39l2j0l4j46j69i60.1793j1j7&sourceid=chrome&ie=UTF-8"
                res = requests.get(url)
                print("Searching...\n")
                soup = BeautifulSoup(res.text, 'html.parser')
                location = soup.select('#wob_loc')[0].getText().strip()
                time = soup.select('#wob_dts')[0].getText().strip()
                info = soup.select('#wob_dc')[0].getText().strip()
                weather = soup.select('#wob_tm')[0].getText().strip()
                speak(f"Location: {location}\nTime: {time}\nWeather: {weather}°F\nInfo: {info}")
            except Exception as e:
                print(e)
                speak("Sorry, unable to fetch weather information for the requested city.")

        elif 'bye' in query:
            speak("Goodbye!")
            exit()

        elif 'thank you' in query:
            speak("You're welcome!")
        elif 'open notepad' in query:
            speak("Sure, opening Notepad.")
            os.startfile("notepad.exe")
            speak("What message should I write for you?")
            message = takeCommand()
            if message != 'None':
                notepad = os.startfile("notepad.exe")
                notepad_app = Application().connect(path="notepad.exe")
                notepad_window = notepad_app.top_window()
                notepad_window.type_keys(message)

        elif 'ask' in query:
            speak("What do you want to ask?")
            question = takeCommand()
            if question != 'None':
                pywhatkit.search(question)
        else:
            speak("Sorry, I didn't get that. Can you please repeat?")
        engine.stop()