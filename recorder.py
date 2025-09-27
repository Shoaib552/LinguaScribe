# recorder.py
import speech_recognition as sr

def record_from_mic(phrase_time_limit=20, timeout=None):
    """
    Record from the default microphone and return an sr.AudioData object.
    phrase_time_limit = max seconds for a single phrase (None for indefinite)
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... (1s)")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Start speaking (will stop after phrase_time_limit or silence)...")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return audio
