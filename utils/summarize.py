import os
from dotenv import find_dotenv, load_dotenv
import openai
# Load environment variables from .env
load_dotenv(find_dotenv(raise_error_if_not_found=True))

# Access the API key
openai.api_key = os.environ["AUDIO_SUMMARY"]

def summarize_gpt(transcript):
    
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
    
    