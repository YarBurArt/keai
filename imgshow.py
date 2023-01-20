from tkinter import Tk, Label
from PIL import ImageTk, Image
import text2audio


def showimg_tk(image_path, text):
    root = Tk()
    root.title("rei emotion")

    loadedfile_img = Image.open(image_path)
    image_no_1 = ImageTk.PhotoImage(loadedfile_img)
    label = Label(image=image_no_1)
    label.grid(row=1, column=0, columnspan=3)
    
    text2audio.playtext(text)

    root.after(2000, root.destroy)
    root.mainloop()


if __name__ == "__main__":
    showimg_tk("graphics/r1.png", "hello world")
