import imgshow
import os
import random
import speech_recognition

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую'],
        'name':['кто ты','кто ты такая', 'что ты'],
        'ext': ['уйди', 'выход', 'замолчи', 'пока', 'досвидания'],
        'wdoing':['у меня всё хорошо', 'нормально']
    }
}
def wdoing():
    imgshow.show("graphics/r1.png", "I'm also doing well")
def name():
    imgshow.show("graphics/r3.png", "I am artificial intelligence Ayanami Rei")
def ext():
    imgshow.show("graphics/r1.png", "goodbye man")
    exit()
def listen_command():
    """The function will return the recognized command"""

    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()

        return query
    except speech_recognition.UnknownValueError:
        imgshow.show("graphics/r2.png", "I don't understand what you mean")


def greeting():
    imgshow.show("graphics/r1.png", "hello man, how are you doing")

def main():
    query = listen_command()

    for k, v in commands_dict['commands'].items():
        if query in v:
            print(globals()[k]())


if __name__ == '__main__':
    while True:
        main()
