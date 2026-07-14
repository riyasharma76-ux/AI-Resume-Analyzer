from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
import fitz
import json
import os

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5175",
    "https://ai-resume-analyzer-f21v.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API is running 🚀"}


@app.get("/test-ai")
def test_ai():
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": "Say hello to Riya in one sentence."
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }


@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):

    # Read uploaded PDF
    pdf = fitz.open(stream=await file.read(), filetype="pdf")

    # Extract text from PDF
    resume_text = ""

    for page in pdf:
        resume_text += page.get_text()

    # AI Prompt
    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the following resume.

Return ONLY a valid JSON object.

Do not write any explanation.
Do not use markdown.
Do not use ```json.

Return exactly in this format:

{{
  "ats_score": 0,
  "strengths": [],
  "weaknesses": [],
  "missing_skills": [],
  "suggestions": [],
  "job_roles": [],
}}

Resume:

{resume_text}
"""

    # Send to Groq
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Get AI response
    analysis = response.choices[0].message.content

    # Remove markdown if AI accidentally returns it
    analysis = analysis.replace("```json", "")
    analysis = analysis.replace("```", "")
    analysis = analysis.strip()

    # Convert JSON string into Python dictionary
    try:
        analysis_json = json.loads(analysis)

        return {
            "filename": file.filename,
            "analysis": analysis_json
        }

    except json.JSONDecodeError:

        return {
            "filename": file.filename,
            "error": "AI returned invalid JSON.",
            "raw_response": analysis
        }