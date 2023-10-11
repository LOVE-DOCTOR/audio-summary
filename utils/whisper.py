import os

from dotenv import load_dotenv
from openai import Audio
from tempfile import NamedTemporaryFile

# Load environment variables from .env
load_dotenv()

# Access the API key
openai_api_key = os.getenv("API_KEY")

def transcribe(audio_file):
    audio_object = Audio()
    try:
        transcript = audio_object.transcribe(model='whisper-1', 
                                             file=audio_file,
                                             api_key=openai_api_key)
        return transcript
    
    except Exception as e:
        with NamedTemporaryFile as temp:
            temp.write(audio_file.getvalue())
            temp.seek(0)
            transcript = audio_object.transcribe(model='whisper-1',
                                                 file=audio_file,
                                                 api_key=openai_api_key)
            return transcript
            