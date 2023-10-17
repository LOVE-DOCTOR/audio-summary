import io
import os
from typing import Annotated
import whisper
from dotenv import load_dotenv, find_dotenv
from openai import Audio
from tempfile import NamedTemporaryFile



# Load environment variables from .env
load_dotenv(find_dotenv(raise_error_if_not_found=True))

# Access the API key
openai_api_key = os.environ["AUDIO_SUMMARY"]

# whisper.openai_api_key = openai_api_key



def whisper_transcribe(audio_file):
    # Initialize Audio object
    audio_object = Audio()
    
    # try block
    try:
        # Initialize the transcribe method with the audio_file
        transcript = audio_object.transcribe(model='whisper-1', 
                                             file=audio_file,
                                             api_key=openai_api_key)
        
        # Returns the final transcription
        return transcript
    
    # except block
    except Exception as e:
        
        # write the audio file to a temporary file
        with NamedTemporaryFile() as temp:
            temp.write(audio_file)
            temp.seek(0)
            
            # Initialize the transcribe method with the audio_file
            transcript = audio_object.transcribe(model='whisper-1',
                                                 file=temp.read(),
                                                 api_key=openai_api_key)
            
            # Returns the final transcription
            return transcript