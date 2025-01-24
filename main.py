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
import subprocess
import time
import psutil

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

    speak("I am Jarvis. How may I help you, Sir Kumar Rahul?")

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
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('xyzemail@gmail.com', '##password')
        server.sendmail('xyzemail@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send this email")

def getNewsHeadlines():
    try:
        url = "https://news.google.com/news/rss"
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'xml')
        headlines = soup.find_all('item', limit=5)
        news = []
        for headline in headlines:
            news.append(headline.title.text)
        return news
    except Exception as e:
        print(e)
        return None

def setReminder(reminder, delay):
    speak(f"Reminder set for {delay} seconds.")
    time.sleep(delay)
    speak(f"Reminder: {reminder}")

def closeApplication(app_name):
    for proc in psutil.process_iter():
        if proc.name().lower() == app_name.lower():
            proc.terminate()
            speak(f"{app_name} has been closed.")
            return
    speak(f"{app_name} is not running.")

def getWeather(city_name):
    try:
        url = f"https://www.google.com/search?q=weather+{city_name}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select_one('#wob_loc').text
        time = soup.select_one('#wob_dts').text
        info = soup.select_one('#wob_dc').text
        temperature = soup.select_one('#wob_tm').text
        return location, time, info, temperature
    except Exception as e:
        print(e)
        return None, None, None, None

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
            speak('Welcome to your super computer lab, Sir Kumar Rahul.')
            speak('How are you, sir?')
            speak('Your missile is ready.')

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

        elif 'email to sir' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "abc123@gmail.com"
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry my friend xyz, I am not able to send this email")

        elif 'what is the weather' in query:
            try:
                speak("Please tell me the city name")
                city_name = takeCommand().lower()
                location, time, info, temperature = getWeather(city_name)
                if location:
                    speak(f"Location: {location}")
                    speak(f"Time: {time}")
                    speak(f"Weather: {info}")
                    speak(f"Temperature: {temperature}°C")
                else:
                    speak("Sorry, unable to fetch weather information for the requested city.")
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
                notepad_app = Application().connect(path="notepad.exe")
                notepad_window = notepad_app.top_window()
                notepad_window.type_keys(message)

        elif 'ask' in query:
            speak("What do you want to ask?")
            question = takeCommand()
            if question != 'None':
                pywhatkit.search(question)

        elif 'open calculator' in query:
            speak("Opening Calculator")
            subprocess.Popen('calc.exe')

        elif 'news headlines' in query:
            speak("Fetching the latest news headlines.")
            headlines = getNewsHeadlines()
            if headlines:
                for headline in headlines:
                    speak(headline)
            else:
                speak("Sorry, I couldn't fetch the news headlines.")

        elif 'set reminder' in query:
            try:
                speak("What should I remind you about?")
                reminder = takeCommand()
                speak("In how many seconds?")
                delay = int(takeCommand())
                setReminder(reminder, delay)
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't set the reminder.")

        elif 'open paint' in query:
            speak("Opening Paint")
            subprocess.Popen('mspaint.exe')

        elif 'open word' in query:
            speak("Opening Microsoft Word")
            subprocess.Popen('winword.exe')

        elif 'open excel' in query:
            speak("Opening Microsoft Excel")
            subprocess.Popen('excel.exe')

        elif 'open powerpoint' in query:
            speak("Opening Microsoft PowerPoint")
            subprocess.Popen('powerpnt.exe')

        elif 'shutdown' in query:
            speak("Shutting down the system")
            os.system('shutdown /s /t 1')

        elif 'restart' in query:
            speak("Restarting the system")
            os.system('shutdown /r /t 1')

        elif 'lock' in query:
            speak("Locking the system")
            os.system('rundll32.exe user32.dll,LockWorkStation')

        elif 'hibernate' in query:
            speak("Hibernating the system")
            os.system('shutdown /h')

        elif 'close youtube' in query:
            closeApplication("chrome.exe") 

        elif 'close google' in query:
            closeApplication("chrome.exe") 

        elif 'close stack overflow' in query:
            closeApplication("chrome.exe") 

        elif 'close notepad' in query:
            closeApplication("notepad.exe")

        elif 'close calculator' in query:
            closeApplication("calc.exe")

        elif 'close paint' in query:
            closeApplication("mspaint.exe")

        elif 'close word' in query:
            closeApplication("winword.exe")

        elif 'close excel' in query:
            closeApplication("excel.exe")

        elif 'close powerpoint' in query:
            closeApplication("powerpnt.exe")

        else:
            speak("Sorry, I didn't get that. Can you please repeat?")
        engine.stop()