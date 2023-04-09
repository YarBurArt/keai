import pyautogui as pag
from sys import platform
import os 
import time
# rewrite these functions for your PC 
# piece of self-documented code


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


# need add Minecraft, Fortnite start at steam , Genshin
def run_game(game_name: str = "minecraft"):
    if platform == "linux":
        os.system("nudoku")
    if platform == "win32":
        if game_name == "minecraft":
            run_app("tla")
        if game_name == "genshin":
            run_app("gensh")
        if game_name == "fortnite":
            pag.alert(text='Is the epicgames closed in trey?',
                      title='check steam', button='YES')
            run_app("stea")
            time.sleep(17)  # wait for loading steam
            pag.alert(text='Is the gamepad up and running and connected?',
                      title='check gamepad', button='YES')
            time.sleep(2)
            pag.click(461, 577)
            time.sleep(1)
            pag.click(391, 425)
            time.sleep(25)  # wait for loading epicgames
            pag.hotkey("win", "up")
            time.sleep(0.5)
            pag.click(78, 435)
    else:
        pass


# only for development
def check_mouse_position():
    while True:
        time.sleep(2)
        print(pag.position())


def sys_statistics():
    if platform == "linux":
        os.system("htop")
    elif platform == "win32":
        os.system("taskmgr")
    else:
        pass


if __name__ == "__main__":
    print(platform)
    run_game("fortnite")
    # check_mouse_position()

