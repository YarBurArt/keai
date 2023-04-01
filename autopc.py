import pyautogui as pag
from sys import platform
import os 
import time

def run_consol():
    if platform == 'linux': # for KDE
        pag.hotkey("win")
        pag.write("kons")
        time.sleep(0.2)
        pag.click(0, 589)  # edit for your monitor
    else:
        pass

def run_browser(url: str = "https://www.google.com"):
    if platform == "linux":
        os.system("firefox " + url)
    else:
        pass

def run_devkit():
    if platform == "linux":
        os.system("cd 'Документы/code' && code .")
        run_consol()
        run_browser("https://youtu.be/8WVrPXWUkVY") # lofi
    else:
        pass

def run_game():
    pass

def sys_statistics():
    if platform == "linux":
        os.system("htop")
    else:
        pass

if __name__ == "__main__":
    print(platform)
    # test
    # run_consol()
    # run_browser()
    # run_devkit()
    sys_statistics()

