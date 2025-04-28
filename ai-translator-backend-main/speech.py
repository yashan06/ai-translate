import whisper
from gtts import gTTS
import uuid
import os

# Load Whisper model once
asr_model = whisper.load_model("base")

def speech_to_text(audio_path: str) -> str:
    result = asr_model.transcribe(audio_path)
    return result["text"]

def text_to_speech(text: str) -> str:
    output_path = f"tts_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='hi')
    tts.save(output_path)
    return output_path
