# 🧠 ATS Checker API (FastAPI + OpenAI)

This is a simple and production-ready API built using **FastAPI**, powered by the **OpenAI GPT model (`o4-mini-2025-04-16`)**, that evaluates how well a resume matches a job description (ATS score) and suggests improvements.

---

## 🚀 Features

- ✅ Accepts resume & job description as text input
- ✅ Returns ATS score (0–100) and improvement suggestions
- ✅ Uses OpenAI's `o4-mini-2025-04-16` model
- ✅ Rate-limited by IP (5 requests/min) using `slowapi`
- ✅ Environment variable support via `.env`

---

## 🏗️ Tech Stack

- **FastAPI** – API framework
- **OpenAI** – AI model for scoring and suggestions
- **SlowAPI** – IP-based rate limiting
- **python-dotenv** – Environment configuration

---

## 📦 Installation

```bash
git clone https://github.com/your-username/ats-checker-api.git
cd ats-checker-api
pip install -r requirements.txt
```
## 🛠️ Configuration
Create a `.env` file in the root directory with the following content:

```plaintext
OPENAI_API_KEY=your_openai_api_key
```
## 🏃‍♂️ Running the API

```bash
uvicorn main:app --reload
```