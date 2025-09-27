# main.py
import argparse
from transcriber import Transcriber
from recorder import record_from_mic
from exporter import save_txt, save_docx
import os

def main():
    parser = argparse.ArgumentParser(description="LinguaScribe - simple speech-to-text")
    parser.add_argument("--engine", choices=["whisper","google"], default="whisper", help="transcription engine")
    parser.add_argument("--model", default="small", help="whisper model (tiny|base|small|medium|large)")
    parser.add_argument("--file", help="path to audio file")
    parser.add_argument("--mic", action="store_true", help="use microphone")
    parser.add_argument("--lang", default="en-IN", help="language code (ex: en-IN, hi-IN)")
    parser.add_argument("--out", help="output file (path). Use .txt or .docx")
    parser.add_argument("--phrase-time", type=int, default=20, help="max seconds to record from mic phrase")
    args = parser.parse_args()

    if not args.mic and not args.file:
        parser.error("Please provide --mic or --file <path>")

    t = Transcriber(engine=args.engine, whisper_model=args.model)

    try:
        if args.mic:
            audio = record_from_mic(phrase_time_limit=args.phrase_time)
            text = t.transcribe_sr_audio(audio, lang=args.lang)
        else:
            if not os.path.exists(args.file):
                raise FileNotFoundError(f"File not found: {args.file}")
            text = t.transcribe_file(args.file, lang=args.lang)

        print("\n--- Transcription ---\n")
        print(text)
        print("\n---------------------\n")

        if args.out:
            if args.out.lower().endswith(".docx"):
                save_docx(args.out, text)
            else:
                # default to txt
                save_txt(args.out, text)
            print("Saved transcription to:", args.out)

    except Exception as e:
        print("Error during transcription:", str(e))

if __name__ == "__main__":
    main()
