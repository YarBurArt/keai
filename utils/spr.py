# -*- coding: utf-8 -*-
# author's / PythonToday, YarBurArt
from os import listdir, system
from random import choice
from speech_recognition import Recognizer, Microphone, UnknownValueError

# Initialize recognition session
sr = Recognizer()
sr.pause_threshold = .5

# edit if add new func
commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую', 'здравствуй'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'play_music': ['включить музыку', 'запустить музыку']
    }
}


def listen_command() -> str:
    """The function will return the recognized command"""
    try:
        # if recognition speech
        with Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query_cmd = sr.recognize_google(audio_data=audio,
                                            language='ru-RU').lower()
        return query_cmd
    except UnknownValueError:
        return 'Не поняла что ты сказал'


def greeting() -> str:
    return 'Привет хозяин'


def create_task() -> str:
    """The function for add task from voice to todo-list"""
    print('Что добавим в список дел?')
    query_task = listen_command()
    with open('todo-list.txt', 'a') as file:
        file.write(f'❗️ {query_task}\n')
    return f'Задача {query_task} добавлена в todo-list'


def play_music() -> str:
    """The function for play random music from '/music/' dir"""
    files = listdir('music')
    random_file = f'music/{choice(files)}'
    system(f'xdg-open {random_file}')
    file_name = random_file.split("/")[-1]
    return f'Музыка {file_name} 🔊🔊🔊'


if __name__ == '__main__':
    """Start listening and run commands by name from dict"""
    query = listen_command()
    for k, v in commands_dict['commands'].items():
        if query in v:
            print(globals()[k]())
