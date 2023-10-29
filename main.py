import io
import os
import openai
from typing import Annotated
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import Audio
import requests
import uvicorn

description = """
The Whisper ASR Summarizer is an API that allows you to upload audio files 
and automatically provides you with a summarized version of the audio in text format.

"""
app = FastAPI(
    title='Whisper ASR Summarizer',
    description=description,
    summary='Summarize audio'
)

origins = ["*"]
methods = ["POST"]
headers = ["Content-Type"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)


# API key
openai.api_key = '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'
gladia_key = '3132b10f-d352-4449-8178-e9da97fea908'

audio_object = Audio()

def summarize_gpt(transcript: str):
    
    prompt = f"""
    You are an AI agent given the sole task of summarizing an audio transcript which can either be of poor or good quality. The transcript generated from the audio file is given below.
    
    {transcript}.
    
    If the transcript is of poor quality or some words have been poorly transcribed, make sure to guess what the word is supposed to be and return a concise summary which contains all the important information from the transcript.
    
    Make sure that you only provide a summary of the conversation and nothing else. DON'T add any additional words that isn't part of the summary.
    
    """
    
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0301',
        messages=[
            {"role": "system",
             "content": prompt}
            ],
        temperature = 0.0
        )
    
    return response.choices[0].message.content
    
def gladia_transcribe(audio_file, filename, content_type):
    

    
    headers = {
        'x-gladia-key': f'{gladia_key}'
    }
    
    files = {'audio': (filename, audio_file, content_type)}
    
    response = requests.post('https://api.gladia.io/audio/text/audio-transcription/', headers=headers, files=files)
    
    return response.json()

def whisper_transcribe(audio_file):
    
    # Initialize the transcribe method with the audio_file
    transcript = audio_object.transcribe(model='whisper-1', 
                                            file=audio_file,
                                            api_key=openai.api_key)
    
    # Returns the final transcription
    return transcript

@app.get('/', tags=['home'])
def home():
    return "OK"

@app.post('/whisper-transcribe/', status_code=200)
async def whisper(file: UploadFile):
    # Read the uploaded audio into BytesIO
    audio_file = io.BytesIO(await file.read())
    
	# Assign the filename to the name parameter of the BytesIO object
    audio_file.name = file.filename

        # Initialize Audio object
    audio_object = Audio()

    # Initialize the transcribe method with the audio_file
    transcript = audio_object.transcribe(model='whisper-1', 
                                                file=audio_file,
                                                api_key=openai.api_key)

    # Returns the final transcription
    return transcript

@app.post('/summarize/')
def summarize(transcript: str):
    
    prompt = f"""
    You are an AI agent given the sole task of summarizing an audio transcript which can either be of poor or good quality. The transcript generated from the audio file is given below.
    
    {transcript}.
    
    If the transcript is of poor quality or some words have been poorly transcribed, make sure to guess what the word is supposed to be and return a concise summary which contains all the important information from the transcript.
    
    Make sure that you only provide a summary of the conversation and nothing else. DON'T add any additional words that isn't part of the summary.
    
    """
    
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0301',
        messages=[
            {"role": "system",
             "content": prompt}
            ],
        temperature = 0.0
        )
    
    return response.choices[0].message.content

@app.post('/gladia/')
async def gladia(file: UploadFile):
    
    # read the uploaded file
    audio_file = await file.read()
    
    # set the filename
    filename = file.filename
    
    # set the content type
    content_type = file.content_type
    
    # Define API key as an header    
    headers = {
        'x-gladia-key': f'{gladia_key}'
    }
    
    # Declare filename, file and content type as a file for the API
    files = {'audio': (filename, audio_file, content_type)}
    
    # Pass the headers and files and send as a request
    response = requests.post('https://api.gladia.io/audio/text/audio-transcription/', headers=headers, files=files)
    
    # convert response to json
    response = response.json()
    
    # Retrieve each transcripted sentence defined by a full stop from the resulting dictionary
    sentences = [item["transcription"] for item in response["prediction"]]
    
    # Extract them from a list and join them together to form a full sentence
    transcript = " ".join(sentences)
    
    return transcript

@app.post('/upload-audio-whisper/')
async def transcribe_summarize_whisper(file: Annotated[UploadFile, File(description="An audio file to be transcribe")]):
    
    audio_file = io.BytesIO(await file.read())
    audio_file.name = file.filename
    
    transcript = whisper_transcribe(audio_file)
    
    summary = summarize_gpt(transcript)
    return {
            'Transcript': transcript,
            'Summary': summary
    }

@app.post('/upload-audio-gladia/')
async def transcribe_summarize_gladia(file: Annotated[UploadFile, File(description="An audio file to be transcribe")]):

    audio_file = await file.read()

    transcript = gladia_transcribe(audio_file, file.filename, file.content_type)
    
    # Combining all transcripted sentences
    sentences = [item["transcription"] for item in transcript["prediction"]]
    transcript = " ".join(sentences)

    summary = summarize_gpt(transcript)

    return {
            'Transcript': transcript,
            'Summary': summary
    }
    
    

if __name__ == '__main__':
    uvicorn.run("main:app", port=6760, log_level="info", reload=True)