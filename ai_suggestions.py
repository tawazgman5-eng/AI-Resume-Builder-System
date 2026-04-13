import os
import openai
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set it for OpenAI to use
openai.api_key = openai_api_key

def generate_resume_suggestions(name, job_title, skills):
    prompt = f"""
    Create a professional summary and suggest additional relevant skills for {name}, 
    who is applying for a {job_title} role. Current listed skills: {skills}.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response['choices'][0]['message']['content']

