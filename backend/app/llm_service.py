import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# =========================================================
# CONFIGURATION
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BACKEND_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Please configure it in backend/.env"
    )

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

client = Groq(
    api_key=GROQ_API_KEY,
    timeout=90.0,
    max_retries=2
)


# =========================================================
# LLM SERVICE
# =========================================================

def ask_llm(prompt: str) -> str:
    """
    Send a prompt to GroqCloud and return the generated response.

    Keeps the existing ask_llm interface compatible with
    resume_optimizer.py and resume_rewriter.py.
    """

    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string.")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=8192
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Groq returned an empty response.")

    return content
