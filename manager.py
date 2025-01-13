#!/usr/bin/env python
"""
 __   __        ___           _       _
 \ \ / /_ _ _ _| _ )_  _ _ _ /_\  _ _| |_
  \ V / _` | '_| _ \ || | '_/ _ \| '_|  _|
   |_|\__,_|_| |___/\_,_|_|/_/ \_\_|  \__|
This is just the code sketch
                        TODO:
- write the exit button
- add hand recognition
- compile 3 types of user signal into one => answer rei
- write a text generation engine based on extended gpt2 conversations waifu
- make normal architecture
- optimization and refactoring
"""

import ipc
import asyncio
from imgshow import showimg_tk
from chatKeai import get_llm_text  # rewtite
from autopc import execute_command
from deep_translator import GoogleTranslator
from spr3 import voice_recognition
from config import commands
from speech_recognition.exceptions import UnknownValueError

# template's translation 
translator = GoogleTranslator(source='ru', target='en')
translator1 = GoogleTranslator(source='en', target='ru')


async def check_voice() -> None:
    """
    The function which processes the voice
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
                text = get_llm_text("This text from my voice recognition: " + translated)
                showimg_tk("graphics/r1.png", text, ismuz=True)
        except UnknownValueError:
            pass
        finally:
            print("end ")


async def check_emotion(ipccntx) -> None:
    """
    The function that takes the recognized emotion from emorec.py,
    recognition in emorec.py must be run in parallel via anaconda
    """
    try:
        ipccntx.wait()
    except AssertionError as e:
        print(e)
    while True:
        await asyncio.sleep(0.5)
        try:
            data = ipccntx.read_data()
            print("from connected user: " + str(data))
            if data == "Happy":  # bug
                # text = get_gpt2_text("tell me like my anime girl: hello, i feel happy")
                text = "null"
                showimg_tk("graphics/r1.png", text, ismuz=True)
        except AssertionError as e:
            print(e)


if __name__ == "__main__":
    try:
        ipc_context = ipc.IpcContext('MySecret')

        # async loop so REI can see and listen me
        loop = asyncio.get_event_loop()
        cors = asyncio.wait([check_voice(), check_emotion(ipccntx=ipc_context)])
        loop.run_until_complete(cors)
    except AssertionError as e:
        print(e)
    except KeyboardInterrupt as e:
        if input("Show traceback if it's an error ? (y/n) : ") in ["y", "Y", "yes", "Yes"]:
            print(e)
        else:
            print("Goodbye, but I wish you wouldn't shut me down like that")
