import speech_recognition as sr
# I have only now got pyaudio working, it's a blessing)))

recognizer_speech = sr.Recognizer()


def voice_recognition(language: str = "en") -> str:
    """
    The function for recording and recognition voice
    :param language: en, ru
    :return: text recognition voice
    """
    with sr.Microphone() as source:
        recognizer_speech.adjust_for_ambient_noise(source)
        audio = recognizer_speech.listen(source)
    text_v = recognizer_speech.recognize_google(audio, language=language)
    return str(text_v)


if __name__ == "__main__":
    text = voice_recognition()
    print(text)
