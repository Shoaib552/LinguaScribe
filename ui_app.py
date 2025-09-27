# ui_app.py
import streamlit as st
import tempfile
from transcriber import Transcriber
from exporter import save_txt, save_docx

# --- Page Config ---
st.set_page_config(
    page_title="LinguaScribe 🎤",
    page_icon="🎧",
    layout="wide"
)

# --- Custom CSS (Glassmorphism) ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #667eea, #764ba2);
        font-family: 'Segoe UI', sans-serif;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 800px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        color: #fff;
    }
    .glass-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .glass-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .glass-header p {
        font-size: 1.2rem;
        opacity: 0.85;
    }
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #fff !important;
        font-size: 1.1rem !important;
        border-radius: 12px !important;
    }
    .stDownloadButton button, .stButton button {
        background: rgba(255, 255, 255, 0.2) !important;
        border: none !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        color: #fff !important;
        cursor: pointer !important;
        transition: all 0.3s ease-in-out;
    }
    .stDownloadButton button:hover, .stButton button:hover {
        background: rgba(255, 255, 255, 0.35) !important;
        transform: translateY(-2px);
    }
    .sidebar .sidebar-content {
        background: rgba(255,255,255,0.15) !important;
        backdrop-filter: blur(12px);
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Content ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown("""
<div class="glass-header">
    <h1>LinguaScribe 🎤</h1>
    <p>Convert your speech into text effortlessly in multiple languages</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Settings ---
st.sidebar.header("⚙️ Settings")
engine = st.sidebar.selectbox("Engine", ["whisper", "google"])
model = st.sidebar.selectbox("Whisper model", ["tiny", "base", "small", "medium", "large"])
lang = st.sidebar.selectbox(
    "Language",
    ["en-IN", "en-US", "hi-IN", "fr-FR", "es-ES", "de-DE"]
)

# --- File Upload ---
uploaded_file = st.file_uploader(
    "🎵 Upload your audio file (mp3, wav, m4a, flac)",
    type=["wav", "mp3", "m4a", "flac"]
)

# --- Transcribe Button ---
if uploaded_file:
    if st.button("🚀 Transcribe Now"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        st.info("⏳ Transcribing... Please wait")

        t = Transcriber(engine=engine, whisper_model=model)
        try:
            text = t.transcribe_file(tmp_path, lang=lang)

            st.success("✅ Transcription Complete!")

            st.text_area("📝 Transcription Result", text, height=300)

            col1, col2 = st.columns(2)
            with col1:
                if st.download_button("📄 Download TXT", text, file_name="transcription.txt"):
                    st.toast("TXT downloaded", icon="📄")
            with col2:
                docx_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
                save_docx(docx_path, text)
                with open(docx_path, "rb") as f:
                    if st.download_button("📑 Download DOCX", f, file_name="transcription.docx"):
                        st.toast("DOCX downloaded", icon="📑")

        except Exception as e:
            st.error("❌ Error: " + str(e))

st.markdown('</div>', unsafe_allow_html=True)
