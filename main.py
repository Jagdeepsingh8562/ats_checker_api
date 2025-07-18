from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class ATSRequest(BaseModel):
    resume: str
    job_description: str

@app.post("/check-ats")
@limiter.limit("5/minute")
async def check_ats(data: ATSRequest, request: Request):
    try:
        system_prompt = (
            "You are an ATS (Applicant Tracking System) assistant. "
            "You receive a resume and job description, and return an ATS match score from 0 to 100. "
            "You also provide suggestions to improve the resume to better match the job description. "
            "Respond in JSON with 'score' (number) and 'suggestions' (list of bullet points)."
        )

        user_content = f"""
Job Description:
{data.job_description}

Resume:
{data.resume}
"""

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.4
        )

        ai_reply = response.choices[0].message.content
        return {"result": ai_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
