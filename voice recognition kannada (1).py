import speech_recognition as sr
import sounddevice as sd
import wave
import numpy as np

import pygame
import time
from gtts import gTTS
from mutagen.mp3 import MP3
import time

from googletrans import Translator
translator = Translator()

def Play(text):
    print(text)
    myobj = gTTS(text=text, lang='en', tld='com', slow=False)
    myobj.save("voice.mp3")
    print('\n------------Playing--------------\n')
    song = MP3("voice.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load('voice.mp3')
    pygame.mixer.music.play()
    time.sleep(song.info.length)
    pygame.quit()


Play("ಸುಸ್ವಾಗತ")

while True:
    duration = 5
    fs = 44100
    channels=2
    filename="input_audio.wav"
    Play("ಏನಾದರು ಹೇಳು")
    
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
            text = recognizer.recognize_google(audio_data, language="kn")
            text = text.lower()
            print("Recognized text:", text)
            ansr = "result not found"
            if text == "ನೀವು ಹೇಗಿದ್ದೀರಿ":
                ansr = "ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ"

            if text == "who are you":
                ansr = "i am a human"

            if text == "how are you":
                ansr = "i am fine"

            if text == "how are you":
                ansr = "i am fine"

            Play(text)
            Play(ansr)
            
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
