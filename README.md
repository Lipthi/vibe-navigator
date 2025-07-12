# Vibe Navigator: Your AI-Powered City Explorer

Vibe Navigator is a hackathon project that helps you explore the vibe of any city,
powered by AI and real Reddit reviews. Just enter a city, category (like café, restaurant), and your vibe preference 
(like cozy or aesthetic), or ask a natural question like "Suggest me a cozy cafes in Bangalore" and the system will recommend the best places.


## Features:

Natural language or structured input support
Summarizes Reddit reviews using Ollama + FastAPI
Recommends aesthetic/cozy/lively places with tags
Clean and responsive frontend (React)
Publicly accessible via Vercel (frontend) + Ngrok (backend)


## Tech Stack

 Frontend: React + CSS                      

 Backend: FastAPI + Python 
 AI Model : Ollama (Gemma 2B) 
  Data Source: Reddit (search API) 


##Running the App Locally

###Prerequisites:
Node.js & npm (for frontend)
Python 3.10+ (for backend)
Ollama installed and running locally
Ngrok for public backend URL

### 1. Clone the repo
`cd frontend`
`npm install`
`npm run dev`

`cd ../backend`
`pip install -r requirements.txt`
`ollama run gemma:2b`
`uvicorn main:app --reload`

`ngrok http 8000`

## Connect Frontend to Backend
`const res = await fetch(`https://your-ngrok-url.ngrok-free.app/summarize?...`);`
