import speech_recognition as sr
from speech_recognition.exceptions import UnknownValueError
# I have only now got pyaudio working, it's a blessing)))

recognizer_speech = sr.Recognizer()


def voice_recognition(language: str = "en") -> str:
    """
    The function for recording and recognition voice
    :param language: en, ru
    :return: text recognition voice
    """
    print('--- start rec')
    with sr.Microphone() as source:
        # recognizer_speech.adjust_for_ambient_noise(source, duration=10)
        audio = recognizer_speech.listen(source)
    print('--- stop rec')
    text_v = recognizer_speech.recognize_google(audio, language=language)
    return str(text_v)


if __name__ == "__main__":
    while True:
        try:
            text = voice_recognition()
            print(text)
            quit() if text == "stop" else ''
        except UnknownValueError:
            print("--- can't recognize or nothing")
