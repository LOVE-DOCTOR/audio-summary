import io
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils.gladia import gladia_transcribe
from utils.summarize import summarize_gpt

from utils.whisper import whisper_transcribe

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)

@app.get('/', tags=['home'], status_code=200)
def home():
    return "Everything is Okay"


@app.post('/upload-audio-whisper/', tags=['upload'], status_code=200)
async def transcribe_summarize_whisper(file: Annotated[UploadFile, File(description="An audio file to be transcribe")]):
    
    audio_file = io.BytesIO(await file.read())
    audio_file.name = file.filename
    
    print('Transcribing uploaded audio')
    transcript = whisper_transcribe(audio_file)
    print(f'Transcript: {transcript}')
    
    print(' ')
    print('Summarizing transcript')
    summary = summarize_gpt(transcript)
    print(f'Summary: {summary}')
    
    return {
            'Transcript': transcript,
            'Summary': summary
    }

@app.post('/upload-audio-gladia/', tags=['upload'], status_code=200)
async def transcribe_summarize_gladia(file: Annotated[UploadFile, File(description="An audio file to be transcribe")]):

    audio_file = await file.read()

    print('Transcribing uploaded audio')
    transcript = gladia_transcribe(audio_file, file.filename, file.content_type)
    
    # Combining all transcripted sentences
    sentences = [item["transcription"] for item in transcript["prediction"]]
    transcript = " ".join(sentences)
    print(f'Transcript: {transcript}')

    print(' ')
    print('Summarizing transcript')
    summary = summarize_gpt(transcript)
    summary = summary.replace('Summary: ', '')
    print(f'Summary: {summary}')

    return {
            'Transcript': transcript,
            'Summary': summary
    }

