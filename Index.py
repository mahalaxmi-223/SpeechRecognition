import webbrowser
import os
from datetime import datetime
import nltk
import pyttsx3
import speech_recognition as sr
import requests

# Initialize pyttsx3 for text-to-speech
zira = pyttsx3.init('sapi5')
voices = zira.getProperty('voices')
zira.setProperty('voice', voices[1].id)

def tell(noise):
    zira.say(noise)
    zira.runAndWait()

def get_synonyms(word):
    synonyms = set(["open", "launch", "start", "run"])
    for syn in nltk.corpus.wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

def greeting():
    date = datetime.now()
    hour = int(date.strftime("%H"))
    if hour >= 0 and hour < 12:
        tell("Good Morning")
    elif hour >= 12 and hour < 16:
        tell("Good Afternoon")
    elif hour >= 16 and hour < 20:
        tell("Good Evening")
    else:
        tell("Hello night user!!!")

def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        location = data['loc'].split(',')
        return {"latitude": location[0], "longitude": location[1]}
    except requests.RequestException as e:
        print('An error occurred:', e)
        return None

def get_weather(lat, lon):
    api_key = "41fdba5b4b3327aef77eb0b61d51f198"
    url = "http://api.openweathermap.org/data/2.5/weather"
    param = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(url, param)
        response.raise_for_status()
        data = response.json()

        if data['cod'] == 200:
            temp = data['main']['temp']
            weather = data['weather'][0]['description']
            tell(f"The temperature is {temp} degree Celsius and the weather is {weather}")
        else:
            tell("Could not retrieve data")
    except requests.RequestException as e:
        tell("An error occurred while fetching weather data")

def command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 0.8
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(e)
            return 'Some error occurred, please try later'

if __name__ == '__main__':
    greeting()
    sites = [
        ['youtube', 'https://youtube.com'],
        ['wikipedia', 'https://wikipedia.com'],
        ['google', 'https://google.com'],
        ['chat gpt', 'https://openai.com']
    ]
    open_synonym = get_synonyms('open')
    weather_synonym = get_synonyms('weather')
    print(weather_synonym)

    while True:
        print("Listening........")
        query = command()
        if query:
            found = False

            # Check for opening websites
            for site in sites:
                for synonym in open_synonym:
                    if f"{synonym} {site[0]}".lower() in query.lower():
                        tell(f'Opening {site[0]}')
                        webbrowser.open(site[1])
                        found = True
                        break

            # Play music if found
            if not found:
                for synonym in open_synonym:
                    if f"{synonym} music" in query:
                        music = "C:\\Users\\Maha\\Music\\My Music\\[iSongs.info] 01 - Tharagathi Gadhi.MP3"
                        os.startfile(music)
                        found = True
                        break

            # Get weather information if found
            if not found:
                for synonym in weather_synonym:
                    if f"{synonym}".lower() in query.lower():
                        location = get_location()
                        if location:
                            lat = location['latitude']
                            lon = location['longitude']
                            get_weather(lat, lon)
                            found = True
                            break

            # If no command found
            if not found:
                tell("Command not found")

