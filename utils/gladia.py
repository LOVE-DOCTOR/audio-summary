import os
from dotenv import find_dotenv, load_dotenv
import requests





def gladia_transcribe(audio_file, filename, content_type):
    
    # Load environment variables from .env
    load_dotenv(find_dotenv(raise_error_if_not_found=True))
    
    # Access the API key
    gladia_key = os.environ["AUDIO_SUMMARY_GLADIA"]
    
    headers = {
        'x-gladia-key': f'{gladia_key}'
    }
    
    files = {'audio': (filename, audio_file, content_type)}
    
    response = requests.post('https://api.gladia.io/audio/text/audio-transcription/', headers=headers, files=files)
    
    return response.json()