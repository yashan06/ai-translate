from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from translation import translate_text
from speech import speech_to_text, text_to_speech
import shutil
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the AI Translator API!"}

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate/text")
def text_translate(req: TranslateRequest):
    translated = translate_text(req.text)
    return {"translated_text": translated}

@app.post("/translate/audio")
async def audio_translate(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = speech_to_text(temp_path)
    translated = translate_text(text)
    os.remove(temp_path)
    
    return {"input_text": text, "translated_text": translated}

@app.post("/tts")
async def tts(req: TranslateRequest):
    mp3_path = text_to_speech(req.text)
    return FileResponse(mp3_path, media_type="audio/mpeg", filename=mp3_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

