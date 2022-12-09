from gtts import gTTS
from playsound import playsound

text = "Hello man, how are you?"

obj = gTTS(text=text, lang='en', slow=False)
obj.save("text.mp3")
playsound("text.mp3")

