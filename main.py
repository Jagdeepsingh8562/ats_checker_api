from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config import OPENAI_API_KEY, OPENAI_MODEL , SYSTEM_PROMPT
from fastapi.middleware.cors import CORSMiddleware

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["https://your-frontend-domain.com"] for production
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the ATS Checker API. Use /check-ats endpoint to check ATS compatibility."}
    

class ATSRequest(BaseModel):
    resume: str
    job_description: str

@app.post("/")
@limiter.limit("5/day")
async def check_ats(data: ATSRequest, request: Request):
    try:
        system_prompt = SYSTEM_PROMPT.strip()

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
        app.logger.error(f"Error processing request: {str(e)}")

        raise HTTPException(status_code=500, detail=str(e))
