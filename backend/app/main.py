from pathlib import Path
import os
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.parser.resume_parser import extract_resume_text
from app.analyzer.resume_analyzer import analyze_resume
from app.ats.ats_analyzer import analyze_job_description
from app.resume_optimizer import optimize_resume
from app.resume_generator import generate_resume_docx
from app.auth import get_current_user


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="ATS Resume Optimizer API",
    description="AI-powered resume optimization platform",
    version="0.1.0",
)


# =========================================================
# CORS
# =========================================================

# Configure additional origins with CORS_ORIGINS (comma-separated).
# Keep localhost defaults for local development. Do not use "*" in production.
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "10")) * 1024 * 1024

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DIRECTORIES
# =========================================================

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


async def save_upload_with_limit(file: UploadFile, destination: Path) -> None:
    """Save an upload in chunks and reject files larger than MAX_UPLOAD_BYTES."""
    total = 0
    try:
        with destination.open("wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_UPLOAD_BYTES:
                    raise HTTPException(
                        status_code=413,
                        detail=f"File is too large. Maximum size is {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.",
                    )
                buffer.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        await file.close()


# =========================================================
# REQUEST MODELS
# =========================================================

class JobDescriptionRequest(BaseModel):
    resume_text: str
    job_description: str


class OptimizeResumeRequest(BaseModel):
    resume_text: str
    job_description: str


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "ATS Resume Optimizer API is running"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# UPLOAD RESUME
# =========================================================

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), current_user=Depends(get_current_user)):

    allowed_extensions = {
        ".pdf",
        ".docx",
    }

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    file_path = UPLOAD_DIR / unique_filename

    try:

        # Save upload with a server-side size limit
        await save_upload_with_limit(file, file_path)

        # Extract text
        resume_text = extract_resume_text(
            str(file_path)
        )

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        return {
            "filename": file.filename,
            "status": "success",
            "character_count": len(resume_text),
            "resume_text": resume_text,
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process resume: {str(error)}"
        )

    finally:

        # Delete temporary uploaded file
        if file_path.exists():
            file_path.unlink()


# =========================================================
# ANALYZE RESUME
# =========================================================

@app.post("/analyze-resume")
async def analyze_uploaded_resume(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):

    allowed_extensions = {
        ".pdf",
        ".docx",
    }

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    file_path = UPLOAD_DIR / unique_filename

    try:

        # Save upload with a server-side size limit
        await save_upload_with_limit(file, file_path)

        # Extract resume text
        resume_text = extract_resume_text(
            str(file_path)
        )

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        # Analyze resume
        analyzed_resume = analyze_resume(
            resume_text
        )

        return {
            "status": "success",
            "resume": analyzed_resume,
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze resume: {str(error)}"
        )

    finally:

        if file_path.exists():
            file_path.unlink()


# =========================================================
# ANALYZE JOB DESCRIPTION
# =========================================================

@app.post("/analyze-jd")
async def analyze_jd(
    request: JobDescriptionRequest,
    current_user=Depends(get_current_user),
):

    if not request.resume_text.strip():

        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty."
        )

    if not request.job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    try:

        result = analyze_job_description(
            request.resume_text,
            request.job_description,
        )

        return {
            "status": "success",
            "analysis": result,
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(error)}"
        )


# =========================================================
# OPTIMIZE RESUME
# =========================================================

@app.post("/optimize-resume")
def optimize_resume_endpoint(
    request: OptimizeResumeRequest,
    current_user=Depends(get_current_user),
):

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not request.resume_text.strip():

        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty."
        )

    if not request.job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    try:

        # -------------------------------------------------
        # AI RESUME OPTIMIZATION
        # -------------------------------------------------

        result = optimize_resume(
            resume_text=request.resume_text,
            job_description=request.job_description
        )

        if not isinstance(result, dict):

            raise HTTPException(
                status_code=500,
                detail="Invalid optimizer response."
            )

        # -------------------------------------------------
        # GET REWRITTEN RESUME
        # -------------------------------------------------

        rewritten_resume = result.get(
            "rewritten_resume"
        )

        if not rewritten_resume:

            raise HTTPException(
                status_code=500,
                detail="Rewritten resume was not generated."
            )

        # -------------------------------------------------
        # GENERATE DOCX
        # -------------------------------------------------

        output_filename = (
            f"generated_resume_{current_user.id}_{uuid.uuid4()}.docx"
        )

        output_path = (
            OUTPUT_DIR / output_filename
        )

        generated_file = generate_resume_docx(
            rewritten_resume,
            str(output_path)
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "status": "success",

            "ats_score": result.get(
                "ats_score"
            ),

            "analysis": {

                "overall_assessment":
                    result.get(
                        "overall_assessment"
                    ),

                "matched_keywords":
                    result.get(
                        "matched_keywords",
                        []
                    ),

                "missing_keywords":
                    result.get(
                        "missing_keywords",
                        []
                    ),

                "warnings":
                    result.get(
                        "warnings",
                        []
                    ),
            },

            "rewritten_resume":
                rewritten_resume,

            "generated_file":
                generated_file,

            "download_url":
                f"/download-resume/{output_filename}",
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Resume optimization failed: {str(error)}"
        )


# =========================================================
# DOWNLOAD GENERATED RESUME
# =========================================================

@app.get("/download-resume/{filename}")
def download_resume(
    filename: str,
    current_user=Depends(get_current_user),
):
    # Reject path traversal and filenames outside the generated-file format.
    safe_filename = Path(filename).name

    if safe_filename != filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename.",
        )

    owner_prefix = f"generated_resume_{current_user.id}_"

    if not safe_filename.startswith(owner_prefix):
        raise HTTPException(
            status_code=404,
            detail="Generated resume not found.",
        )

    # Validate the UUID suffix.
    suffix = safe_filename[len(owner_prefix):]

    if not suffix.endswith(".docx"):
        raise HTTPException(
            status_code=404,
            detail="Generated resume not found.",
        )

    try:
        uuid.UUID(suffix[:-5])
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Generated resume not found.",
        )

    file_path = OUTPUT_DIR / safe_filename

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Generated resume not found.",
        )

    return FileResponse(
        path=file_path,
        filename="optimized_resume.docx",
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    )


