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

# template's translation 
translator = GoogleTranslator(source='ru', target='en')
translator1 = GoogleTranslator(source='en', target='ru')

conn, addres = None # add global
def start(): # add
    # set socket parameters for IPC
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))


async def check_voice():
    """
    The function which processes the voice over recording in seconds
    :return: start app from recognize voice or answer by rei
    """
    while True:
        await asyncio.sleep(0.1)
        print("debug 1")
        text: str = voice_recognition(language='en')  # edit lang for your region
        # if command is not found or else execute it

        print(text)
        print("end ")
        # if not await execute_command(commands, text):
        #     translated = translator.translate(text)
        #     text = get_gpt2_text("tell me how is my anime girl: " + translated)
        #     showimg_tk("graphics/r1.png", text, ismuz=True)


async def check_emotion():
    """
    The function that takes the recognized emotion from emorec.py,
    recognition in emorec.py must be run in parallel via anaconda
    """
    while True:
        await asyncio.sleep(0.5)
        data = conn.recv(1024).decode()
        if not data:
            conn.close(); break  # here lies the error
        print("from connected user: " + str(data))
        if data == "Happy":
            text = get_gpt2_text("tell me how is my anime girl: hello, i feel happy")
            showimg_tk("graphics/r1.png", text, ismuz=True)

if __name__ == "__main__":
    # async loop so REI can see and listen me
    loop = asyncio.get_event_loop()
    cors = asyncio.wait([check_voice(), check_emotion()])
    loop.run_until_complete(cors)
