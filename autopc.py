import pyautogui as pag
from sys import platform
import os 
import time


def run_app(name: str = ""):
    pag.hotkey("win")
    pag.write(name)
    pag.hotkey("enter")


def run_consol():
    if platform == "linux":  # for KDE
        pag.hotkey("win")
        pag.write("kons")
        time.sleep(0.2)
        pag.click(0, 589)  # edit for your monitor
    if platform == "win32":
        run_app("powershell")
    else:
        pass


def run_browser(url: str = "https://www.google.com"):
    if platform == "linux":
        os.system("firefox " + url)
    elif platform == "win32":
        os.system("start " + url)
    else:
        pass


def run_devkit(variant: str = "python"):
    if platform == "linux":
        os.system("cd 'Документы/code' && code .")
        run_consol()
        run_browser("https://youtu.be/8WVrPXWUkVY")  # lofi
    if platform == "win32":
        if variant == "python":
            run_app("pycharm")
            run_browser("https://www.youtube.com/watch?v=T606XQFDNVg&list=PLl578ZPbYIlFcSxuka8Km37VgbUYUWI5p")
        if variant == "c++" or variant == "c#":
            run_app("visual Studio 2022")
            run_browser("https://youtu.be/8T2ZJ6L2YQM")
    else:
        pass


def run_game():
    pass


def sys_statistics():
    if platform == "linux":
        os.system("htop")
    elif platform == "win32":
        os.system("taskmgr")
    else:
        pass


if __name__ == "__main__":
    print(platform)
    # test
    # run_consol()
    # run_browser()
    # run_devkit()
    # sys_statistics()

