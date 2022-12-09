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

def write(str_to_write):
    subprocess.Popen(['/bin/sh', '-c', f'echo "{str_to_write}" | xsel --clipboard --input'])
    pag.hotkey("ctrl","v")

time.sleep(7)

write("кто я")

