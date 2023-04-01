import speech_recognition as sr

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np  # for convert audio flow

import time 


fs = 44100  # Sample rate
seconds = 3  # Duration of recording

recognizer = sr.Recognizer()


def record_audio(sec:int = seconds) -> None:
    # start recording
    data = sd.rec(int(sec * fs), samplerate=fs, channels=2)
    sd.wait() # end recording
    # convert float flow to int array 
    y = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
    write('out.wav', fs, y) # save file   


def recognize_voice(lang:str = "en") -> str:
    file = sr.AudioFile('out.wav') # up file to cache
    with file as source: # open file to flow
        # clean up the noise 
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source) # read audio
        # recognize by google api
        return recognizer.recognize_google(audio, language=lang)


if __name__ == '__main__':
    if input():
        print('start recording')
        record_audio() 
        print('end recording')
        time.sleep(0.2)
        text = recognize_voice(lang='ru')
        print(text)
    