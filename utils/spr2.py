import speech_recognition as sr
from fuzzywuzzy import fuzz, process

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np  # for convert audio flow

import time 


fs = 44100  # Sample rate
seconds = 3  # Duration of recording

recognizer = sr.Recognizer()


def record_audio(sec: int = seconds) -> None:
    """
    The function for recording an audio file
    with a second limit
    """
    # start recording
    data = sd.rec(int(sec * fs), samplerate=fs, channels=2)
    sd.wait()  # end recording
    # convert float flow to int array
    data = data / np.abs(data).max()
    type_max = np.iinfo(np.int32).max
    out_data = (type_max * data).astype(np.int32)
    write('../audio/out.wav', fs, out_data)  # save file


def recognize_voice(lang: str = "en") -> str:
    """
    The function that converts a file to text 
    """
    file = sr.AudioFile('../audio/out.wav')  # up file to cache
    with file as source:  # open file to flow
        # clean up the noise 
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)  # read audio
        # recognize by google api
        return recognizer.recognize_google(audio, language=lang)


if __name__ == '__main__':
    if sec := input("enter sec:"):
        print('start recording')
        # record_audio(int(sec))
        print('end recording')
        time.sleep(0.2)
        text = recognize_voice(lang='ru')
        print(text)
        if fuzz.ratio(text.lower(), 'привет') >= 60:
            print("Hello, world!")
