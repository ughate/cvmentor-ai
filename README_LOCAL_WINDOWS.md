# CV Mentor AI – Resume Optimizer

An AI-powered application that tailors resumes to job descriptions.

## Technology Stack

- Frontend: React 19 + Vite
- Backend: Python + FastAPI
- AI provider: Groq API
- AI model: openai/gpt-oss-20b (configurable)
- Authentication: Supabase Auth
- Resume processing: PDF and DOCX
- Output: Optimized DOCX resume

## Project Structure

- backend/ - FastAPI application
- frontend/ - React application
- backend/app/ - API, authentication, AI and resume services

## Local Development

### Backend

From the project root:

1. Set-Location .\backend
2. .\.venv\Scripts\Activate.ps1
3. python -m pip install -r requirements.txt
4. uvicorn app.main:app --reload

Backend: http://127.0.0.1:8000

Health check: http://127.0.0.1:8000/health

API documentation: http://127.0.0.1:8000/docs

### Frontend

Open another PowerShell window:

1. Set-Location .\frontend
2. npm install
3. npm run dev

Frontend: http://localhost:5173

## Environment Variables

Backend variables:

- GROQ_API_KEY
- GROQ_MODEL
- SUPABASE_URL
- SUPABASE_SECRET_KEY
- CORS_ORIGINS
- MAX_UPLOAD_MB

Frontend variables:

- VITE_API_URL
- VITE_SUPABASE_URL
- VITE_SUPABASE_PUBLISHABLE_KEY

See the .env.example files for templates.

Never expose backend secrets in frontend configuration.

## Planned Production Architecture

- Existing website: https://cvmentor.in
- AI application: https://app.cvmentor.in
- AI API: https://api.cvmentor.in

The existing website and AI application will use separate deployments.

## Security

- Never commit .env files or API keys.
- Keep Groq and Supabase secret keys on the backend.
- Require authenticated API access.
- Review generated resumes for factual accuracy.
- Establish upload validation, retention and deletion policies before public launch.
- Review AI provider privacy and data-handling terms before processing customer resumes.

## Development Status

- Local frontend production build verified.
- Backend and frontend deployment configuration remains to be completed.
- Production hosting and domain configuration are pending.
