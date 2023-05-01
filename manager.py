"""
 __   __        ___           _       _
 \ \ / /_ _ _ _| _ )_  _ _ _ /_\  _ _| |_
  \ V / _` | '_| _ \ || | '_/ _ \| '_|  _|
   |_|\__,_|_| |___/\_,_|_|/_/ \_\_|  \__|
This is just the code sketch
                        TODO:
- add hand recognition
- compile 3 types of user signal into one => answer rei
- write a text generation engine based on extended gpt2 conversations waifu
- make normal architecture
- optimization and refactoring
"""

import socket
import asyncio
from imgshow import showimg_tk
from chatKeai import get_gpt2_text  # rewtite
from autopc import execute_command
from deep_translator import GoogleTranslator
from spr3 import voice_recognition
from config import commands
from speech_recognition.exceptions import UnknownValueError

# template's translation 
translator = GoogleTranslator(source='ru', target='en')
translator1 = GoogleTranslator(source='en', target='ru')


def start_serv() -> tuple:
    # set socket parameters for IPC
    host = socket.gethostname()
    port = 1123
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)

    return server_socket.accept()


async def check_voice() -> None:
    """
    The function which processes the voice over recording in seconds
    :return: start app from recognize voice or answer by rei
    """
    while True:
        await asyncio.sleep(0.1)
        print("debug 1")
        try:
            text: str = voice_recognition(language='en')  # edit lang for your region
            print(text)
            # if command is not found or else execute it
            if not await execute_command(commands, text):
                translated = translator.translate(text)
                text = get_gpt2_text("tell me how is my anime girl: " + translated)
                showimg_tk("graphics/r1.png", text, ismuz=True)
        except UnknownValueError:
            pass
        finally:
            print("end ")


async def check_emotion(connection) -> None:
    """
    The function that takes the recognized emotion from emorec.py,
    recognition in emorec.py must be run in parallel via anaconda
    """
    while True:
        await asyncio.sleep(0.5)
        data = connection.recv(1024).decode()
        if not data:
            connection.close(); break  # here lies the error
        print("from connected user: " + str(data))
        if data == "Happy":
            text = get_gpt2_text("tell me how is my anime girl: hello, i feel happy")
            showimg_tk("graphics/r1.png", text, ismuz=True)

if __name__ == "__main__":
    print("debug 0")
    conn, address = start_serv()
    print("debug end")
    print("Connection from: " + str(address))

    # async loop so REI can see and listen me
    loop = asyncio.get_event_loop()
    cors = asyncio.wait([check_voice()])  # check_emotion(connection=conn)])
    loop.run_until_complete(cors)
