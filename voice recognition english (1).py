import speech_recognition as sr
import sounddevice as sd
import wave
import numpy as np
import pandas as pd
from difflib import SequenceMatcher
import pygame
import time
from gtts import gTTS
from mutagen.mp3 import MP3
import time
import wikipedia
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date

def Play(text1):
    print(text1)
    myobj = gTTS(text=text1, lang='en-us', tld='com', slow=False)
    myobj.save("voice.mp3")
    print('\n------------Playing--------------\n')
    song = MP3("voice.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load('voice.mp3')
    pygame.mixer.music.play()
    time.sleep(song.info.length)
    pygame.quit()


Play("Hello welcome")


while True:
    duration = 5
    fs = 44100
    channels=2
    filename="input_audio.wav"
    Play('Say something')
    
    print("Recording...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype=np.int16)
    sd.wait()
    print("Recording complete.")

    # Save the recorded audio to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())

    # Perform speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            text = text.lower()
            print("Recognized text:", text)
            answer = 'result not found'

            if SequenceMatcher(None,text,'what is date time now').ratio()*100 > 80:
                today1 = datetime.now()
                Time = today1.strftime("%H:%M:%S")
                today2 = date.today()
                Date = today2.strftime("%d-%m-%y")
                answer = 'time is '+Time+'. Date is '+Date
                
            elif 'weather' in text:
                try:
                    
                    # creating url and requests instance
                    url = "https://www.google.com/search?q="+"weather"
                    html = requests.get(url).content

                    # getting raw data
                    soup = BeautifulSoup(html, 'html.parser')
                    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
                    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

                    # formatting data
                    data = str.split('\n')
                    sky = data[1]

                    # getting all div tag
                    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
                    strd = listdiv[5].text

                    # getting other required data
                    pos = strd.find('Wind')
                    other_data = strd[pos:]
                    
                    answer = "Temperature is "+temp+" Sky Description: "+sky+" other_data "+other_data
                except:
                    pass
            else:    
                List = pd.read_csv('English.csv')
                Question = List['question']
                Answer = List['answer']
                A=0
                for qsn in Question:
                    if SequenceMatcher(None,text,qsn).ratio()*100 > 75:
                        answer = List.loc[A]['answer']
                        break
                    A += 1
                else:
                    try:
                        result = wikipedia.search(text)
                        page = wikipedia.page(result[0])
                        title = page.title
                        categories = page.categories 
                        content = page.content
                        links = page.links
                        references = page.references
                        answer = page.summary
                    except:
                        pass
                
            Play(answer)
            
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
