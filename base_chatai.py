import subprocess
import pyautogui as pag
import time
# from pymouse import PyMouse
# from pykeyboard import PyKeyboard
#
# m = PyMouse()
# k = PyKeyboard()
#
# x_dim, y_dim = m.screen_size()
# m.click(x_dim/2, y_dim/2)

# def write(str_to_write):
#     subprocess.Popen(['/bin/sh', '-c', f'echo "{str_to_write}" | xsel --clipboard --input'])
#     pag.hotkey("ctrl","v")
#
# time.sleep(7)
#
# write("кто я")
#
# from keyboard import press_and_release
# from time import sleep
# import pyautogui, pyperclip
#
# def paste(text: str):
#     pyperclip.copy(text)
#     press_and_release('ctrl + v')
#
#
# def type(text: str, interval=0.0):
#     buffer = pyperclip.paste()
#     if not interval:
#         paste(text)
#     else:
#         for char in text:
#             paste(char)
#             sleep(interval)
#     pyperclip.copy(buffer)
#
# type('Привет мир!', 0.1)