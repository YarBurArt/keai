from tkinter import Tk, Label
from PIL.ImageTk import PhotoImage
from PIL.Image import open as open_img
import text2audio


def showimg_tk(image_path, text="rei", ismuz=False):
    """
    The function that shows an image for a couple of seconds 
    and plays speech RAI
    """
    root = Tk()
    root.title("rei emotion")

    loadedfile_img = open_img(image_path)
    image_no_1 = PhotoImage(loadedfile_img)
    label = Label(image=image_no_1)
    label.grid(row=1, column=0, columnspan=3)
    
    if ismuz:
        text2audio.playtext(text)

    root.after(2000, root.destroy)
    root.mainloop()


if __name__ == "__main__":
    showimg_tk("graphics/r1.png", 
               "hello world", ismuz=True)
