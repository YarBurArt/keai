from keai.utils.spr2 import record_audio, recognize_voice
import socket
import asyncio
from imgshow import showimg_tk
from chatKeai import get_gpt2_text  # rewtite
import autopc
from deep_translator import GoogleTranslator

# template's translation 
translator = GoogleTranslator(source='ru', target='en')
translator1 = GoogleTranslator(source='en', target='ru')


async def check_voice():
    """
    The function which processes the voice over recording in seconds
    :return: start app from recognize voice or answer by rei
    """
    while True:
        await asyncio.sleep(3)
        if sec := input("enter sec:"):
            if sec == "q":
                break  # crutch to get out

            # it's highlighted because it's so beautiful ^_^
            with int(sec) as record_sec:
                print('start recording')
                record_audio(record_sec)
                print('end recording')
                await asyncio.sleep(0.2)
                text = recognize_voice(lang='ru')  # edit lang for your region

            # this must be added for levenstein distance
            if "питон" in text.split(" "):
                autopc.run_devkit("python")
            if "плюсы" in text.split(" "):
                autopc.run_devkit("c++")
            if "интернет" in text.split(" "):
                autopc.run_browser()
            if "консоль" in text.split(" "):
                autopc.run_consol()
            if "системы" in text.split(" "):
                autopc.sys_statistics()
            else:
                translated = translator.translate(text)
                text = get_gpt2_text("tell me how is my anime girl: " + translated)
                showimg_tk("graphics/r1.png", text, ismuz=True)

# set socket parameters for IPC
host = socket.gethostname()
port = 5000
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(2)
conn, address = server_socket.accept()
print("Connection from: " + str(address))


async def check_emotion():
    """
    The function that takes the recognized emotion from emorec.py,
    recognition in emorec.py must be run in parallel via anaconda
    """
    while True:
        await asyncio.sleep(0.5)
        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            break  # here lies the error
        print("from connected user: " + str(data))
        if data == "Happy":
            text = get_gpt2_text("tell me how is my anime girl: hello, i feel happy")
            showimg_tk("graphics/r1.png", text, ismuz=True)

# async loop so REI can see and listen me
loop = asyncio.get_event_loop()
cors = asyncio.wait([check_voice(), check_emotion()])
loop.run_until_complete(cors)
