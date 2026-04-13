# ai_engine.py (COMPLETED AND CORRECTED)

import os
import json  # <-- CRITICAL FIX: Missing JSON import
from dotenv import load_dotenv
from openai import OpenAI, APIError  # <-- CRITICAL FIX: Missing APIError import

# --- AI CONFIGURATION ---
load_dotenv()
try:
    # Initialize the OpenAI client using the key from the .env file
    # 'client' is now defined at the module's global scope.
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

# Define the structured output schema (JSON object) for the AI Scanner
SCANNER_SCHEMA = {
    "type": "object",
    "properties": {
        "match_score": {"type": "integer", "description": "Percentage match between the resume and JD (0-100)."},
        "analysis": {"type": "string", "description": "A short, professional paragraph explaining the score."},
        "missing_keywords": {"type": "array", "items": {"type": "string"},
                             "description": "Crucial skills/requirements mentioned in the JD but missing from the resume."},
        "matched_keywords": {"type": "array", "items": {"type": "string"},
                             "description": "Key strengths/skills that match the JD."},
        "suggestions": {"type": "string",
                        "description": "One specific, actionable suggestion to increase the match score, focusing on the missing keywords."},
    },
    "required": ["match_score", "analysis", "missing_keywords", "matched_keywords", "suggestions"],
}


# --- AI-POWERED match_score ---
def match_score_openai(resume_text, job_text):
    """
    Uses GPT-4o-mini to semantically compare resume and job description,
    returning a structured dictionary (JSON equivalent).
    """

    # We rely on the module-level 'client' variable defined above.
    if client is None:
        return {"error": "OpenAI API Client is not initialized. Check your API key in .env"}

    # We include the entire schema definition in the prompt to ensure the AI follows it
    schema_definition = json.dumps(SCANNER_SCHEMA, indent=2)

    prompt = f"""
    You are an expert Talent Acquisition Specialist. Your task is to semantically compare the given RESUME against the JOB DESCRIPTION (JD).

    1. Score the match from 0 to 100.
    2. Identify key missing skills.
    3. Identify strong matching points.
    4. Provide one clear suggestion for improvement.

    JOB DESCRIPTION:
    ---
    {job_text}
    ---

    RESUME TEXT:
    ---
    {resume_text}
    ---

    Return the analysis strictly as a JSON object matching this schema:
    {schema_definition}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are a professional JSON-generating tool that acts as a resume scanner. You must strictly follow the provided JSON schema definition in the user request."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        json_string = response.choices[0].message.content.strip()
        return json.loads(json_string)  # Uses the imported 'json'

    except APIError as e:  # Uses the imported 'APIError'
        return {"error": f"OpenAI API Error: {e.code} - Check your API key and billing status."}
    except Exception as e:
        return {"error": f"An unexpected error occurred during API call: {str(e)}"}