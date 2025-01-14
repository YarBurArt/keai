#!/usr/bin/env python
"""
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
import logging
import asyncio

from imgshow import showimg_tk
from chatKeai import get_llm_text  # rewrite
from autopc import execute_command
from deep_translator import GoogleTranslator
from spr3 import voice_recognition
from config import commands
from speech_recognition.exceptions import UnknownValueError

logging.basicConfig(
    format="{asctime}-{levelname}:{name}:{message}",
    style="{", datefmt="%H:%M:%S"
)

# template's translation 
translator = GoogleTranslator(source='ru', target='en')
translator1 = GoogleTranslator(source='en', target='ru')


async def handle_voice_command(text: str) -> None:
    """execute command or answer"""
    # run_command_pc()
    if not await execute_command(commands, text):
        translated = translator.translate(text)
        response_text = get_llm_text(
            f"This text from my voice recognition: {translated}")
        logging.debug(f"response llm: {response_text}")
        showimg_tk("graphics/r1.png", response_text, ismuz=True)  # with TTS


async def check_voice() -> None:
    """
    The function which processes the voice
    :return: start app from recognize voice or answer by rei
    """
    while True:
        await asyncio.sleep(0.1)
        logging.debug("start check_voice")
        try:
            # edit lang for your region
            text_voice: str = voice_recognition(language='en')
            logging.debug(f"voice: {text_voice}")
            await handle_voice_command(text_voice)

        except UnknownValueError:
            pass
        finally:
            logging.debug("end check_voice")


async def check_emotion(ipccntx: ipc.IpcContext) -> None:
    """
    The function that takes the recognized emotion from emorec.py,
    recognition in emorec.py must be run in parallel via anaconda
    """
    try:
        ipccntx.wait()
    except AssertionError as e:
        logging.error(e)
    while True:
        await asyncio.sleep(0.5)
        try:
            data = ipccntx.read_data()
            logging.debug("from connected user: " + str(data))
            if data == "Happy":  # bug
                text = "null"
                showimg_tk("graphics/r1.png", text, ismuz=True)
        except AssertionError as e:
            logging.error(e)


async def check_pose():
    """ based on handrec or poseimg2txt"""
    pass


async def run_command_pc():
    """wrapper to get command from text"""
    pass


if __name__ == "__main__":
    try:
        logging.info("loaded as main")
        ipc_context = ipc.IpcContext('MySecret')
        logging.debug("loaded ipc ctx")

        # async loop so REI can see and listen me
        loop = asyncio.get_event_loop()
        tasks = [
            check_voice(),
            check_emotion(ipccntx=ipc_context),
            # check_pose()
        ]
        loop.run_until_complete(asyncio.gather(*tasks))
    except AssertionError as e:
        logging.error(e)
    except KeyboardInterrupt as e:
        if input("Show traceback if it's an error ? (y/n) : ") in ["y", "Y", "yes", "Yes"]:
            logging.error(e)
        else:
            print("Goodbye, but I wish you wouldn't shut me down like that")
