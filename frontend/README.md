# CV Mentor AI – Frontend

This directory contains the React + Vite frontend for the CV Mentor AI resume optimizer.

## Technology

- React
- Vite
- Supabase Authentication

## Local Development

Run these commands from the project root:

1. Set-Location .\frontend
2. npm install
3. npm run dev

The development server normally runs at:

http://localhost:5173

## Environment Configuration

Create a local .env.local file using .env.example as the template.

Required variables:

- VITE_API_URL
- VITE_SUPABASE_URL
- VITE_SUPABASE_PUBLISHABLE_KEY

Never put Groq API keys or Supabase secret keys in frontend environment variables.

## Production Build

Run from the frontend directory:

npm run build

The production output is generated in the dist directory.

For complete project setup and deployment information, see the root README_LOCAL_WINDOWS.md.
