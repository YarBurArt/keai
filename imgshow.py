from tkinter import Tk, Label
from PIL import ImageTk, Image

def show(image):
    root = Tk()
    root.title("")
    image_no_1 = ImageTk.PhotoImage(Image.open(image))
    label = Label(image=image_no_1)
    label.grid(row=1, column=0, columnspan=3)
    root.after(5000, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    show("graphics/g2.png")