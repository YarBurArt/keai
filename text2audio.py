from playsound import playsound
from gtts import gTTS


def playtext(text):
    obj = gTTS(text=text, 
               lang='en', 
               slow=False)
    obj.save("text.mp3")
    playsound("text.mp3")


if __name__ == '__main__':
    some_text = "Hello man, how are you?"
    playtext(some_text)
