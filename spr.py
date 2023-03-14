# code by python today for learn sr
from os import listdir, system
from random import choice
from speech_recognition import Recognizer, Microphone, UnknownValueError

sr = Recognizer()
sr.pause_threshold = 0.5

commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую', 'здравствуй'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'play_music': ['включить музыку', 'запустить музыку']
    }
}


def listen_command():
    """The function will return the recognized command"""
    try:
        with Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
        return query
    except UnknownValueError:
        return 'Не поняла что ты сказал'


greeting = lambda x: 'Привет хозяин'


def create_task():
    print('Что добавим в список дел?')

    query = listen_command()
    with open('todo-list.txt', 'a') as file:
        file.write(f'❗️ {query}\n')
        
    return f'Задача {query} добавлена в todo-list'


def play_music():
    files = listdir('music')
    random_file = f'music/{choice(files)}'
    system(f'xdg-open {random_file}')
    file_name = random_file.split("/")[-1]
    return f'Музыка {file_name} 🔊🔊🔊'


if __name__ == '__main__':
    query = listen_command()
    for k, v in commands_dict['commands'].items():
        if query in v:
            print(globals()[k]())
