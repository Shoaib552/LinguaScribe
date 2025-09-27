# streamlit_app.py
import streamlit as st
import tempfile
from transcriber import Transcriber

st.set_page_config(page_title="LinguaScribe", layout="centered")
st.title("LinguaScribe — Speech to Text")

engine = st.selectbox("Engine", ["whisper", "google"])
model = st.selectbox("Whisper model (if using whisper)", ["tiny","base","small","medium","large"])
lang = st.selectbox("Language", ["en-IN","hi-IN","en-US","fr-FR","es-ES"])

uploaded_file = st.file_uploader("Upload audio file (.wav, .mp3, .m4a, .flac)", type=["wav","mp3","m4a","flac"])
if st.button("Transcribe"):
    if not uploaded_file:
        st.warning("Please upload an audio file")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        st.info("Transcribing... this may take a while for large files / big models.")
        t = Transcriber(engine=engine, whisper_model=model)
        try:
            text = t.transcribe_file(tmp_path, lang=lang)
            st.text_area("Transcription", text, height=300)
        except Exception as e:
            st.error("Error: " + str(e))
