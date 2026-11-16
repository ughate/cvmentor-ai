import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

# Load backend/.env regardless of the directory used to start the API
BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is missing from backend/.env")

if not SUPABASE_SECRET_KEY:
    raise RuntimeError("SUPABASE_SECRET_KEY is missing from backend/.env")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY,
)
