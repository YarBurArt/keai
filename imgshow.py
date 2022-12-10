from tkinter import Tk, Label
from PIL import ImageTk, Image
import text2audio

def show(image, text):
    root = Tk()
    root.title("")
    image_no_1 = ImageTk.PhotoImage(Image.open(image))
    label = Label(image=image_no_1)
    label.grid(row=1, column=0, columnspan=3)
    text2audio.playtext(text)
    root.after(2000, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    show("graphics/r1.png", "hello world")