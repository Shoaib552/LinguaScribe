# transcriber.py
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

class Transcriber:
    def __init__(self, engine="whisper", whisper_model="small"):
        """
        engine: "whisper" or "google"
        whisper_model: tiny | base | small | medium | large
        """
        self.engine = engine.lower()
        self.recognizer = sr.Recognizer()
        self.whisper_model = whisper_model
        self._whisper_model_obj = None
        if self.engine == "whisper":
            import whisper
            self._whisper_model_obj = whisper.load_model(whisper_model)

    def _to_wav(self, src_path):
        """Convert any audio file to a WAV file and return path."""
        ext = os.path.splitext(src_path)[1].lower()
        if ext == ".wav":
            return src_path
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio = AudioSegment.from_file(src_path)
        audio.export(tmp.name, format="wav")
        return tmp.name

    def transcribe_file(self, audio_path, lang=None):
        """
        Transcribe an audio file using selected engine.
        lang: language code like "en-IN", "hi-IN", "en-US", or None
        """
        if self.engine == "google":
            wav = self._to_wav(audio_path)
            with sr.AudioFile(wav) as source:
                audio = self.recognizer.record(source)
            # speech_recognition recognizes many language codes; use e.g. "hi-IN"
            return self.recognizer.recognize_google(audio, language=lang or "en-IN")
        elif self.engine == "whisper":
            # whisper prefers short language codes like 'en','hi'
            language_short = None
            if lang:
                language_short = lang.split("-")[0]
            # Whisper can accept mp3/wav directly; use the original
            result = self._whisper_model_obj.transcribe(audio_path, language=language_short) if language_short else self._whisper_model_obj.transcribe(audio_path)
            return result.get("text", "")
        else:
            raise ValueError("Unknown engine: use 'google' or 'whisper'")

    def transcribe_sr_audio(self, sr_audio, lang=None):
        """
        Accepts a speech_recognition.AudioData object (from mic).
        Writes temp wav from it and calls transcribe_file.
        """
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp.write(sr_audio.get_wav_data())
        tmp.flush()
        tmp.close()
        return self.transcribe_file(tmp.name, lang=lang)
