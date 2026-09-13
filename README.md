# 🧠 Node Solutions — AI Request Triage Assistant

> An enterprise-grade AI-powered triage tool designed to classify, prioritize, route, and draft responses for incoming business requests in real-time. Built for the **Node Solutions Technical Challenge (Stage 2)**.

---

## 🌟 Overview

Incoming business communications (support tickets, sales leads, billing inquiries, critical bugs) often arrive unstructured. The **AI Request Triage Assistant** leverages **Google Gemini AI** and a production-ready **FastAPI** backend paired with a **React** interface to analyze incoming requests in seconds.

### Key Capabilities
- **Automated Summarization**: Extracts a concise 1–2 sentence essence of the request.
- **Classification**: Categorizes into `Technical`, `Billing`, `Sales`, `Feature Request`, `Customer Inquiry`, or `General`.
- **Intelligent Prioritization**: Assigns `Low`, `Medium`, `High`, or `Urgent` along with explicit rationale (e.g. data exposure or severe service outage triggers `Urgent`).
- **Smart Routing**: Directs the request to the appropriate internal team (`Engineering`, `Billing Operations`, `Sales Team`, `Product Team`, etc.).
- **Context-Aware Response Drafting**: Drafts professional, empathetic, and situation-tailored responses ready for agent review.
- **Database Persistence**: Stores all historical triage logs in **Supabase PostgreSQL** (with automatic SQLite local fallback).
- **Authentication & Security**: Database-backed authentication with salted PBKDF2 password hashing protecting dashboard access.

---

## 🏗️ Architecture & Tech Stack

```
                     ┌──────────────────────────────────────┐
                     │          React + Vite Frontend       │
                     │   (Node Solutions Theme & Brand)     │
                     └──────────────────┬───────────────────┘
                                        │ REST API calls (Axios)
                                        ▼
                     ┌──────────────────────────────────────┐
                     │        FastAPI Backend Service       │
                     │  ┌────────────────────────────────┐  │
                     │  │ Router (/api/triage, /api/auth)│  │
                     │  ├────────────────────────────────┤  │
                     │  │ Service (Triage & Validation)  │  │
                     │  ├────────────────────────────────┤  │
                     │  │ Prompt Engineering (Gemini API)│  │
                     │  ├────────────────────────────────┤  │
                     │  │ Repository (SQLAlchemy ORM)    │  │
                     │  └────────────────────────────────┘  │
                     └──────────────┬──────────────────┬────┘
                                    │                  │
                SQLAlchemy Session  │                  │  Google Generative AI SDK
                                    ▼                  ▼
                     ┌──────────────────────┐  ┌───────────────────────┐
                     │ Supabase PostgreSQL  │  │ Google Gemini 2.5/3.5 │
                     │  (Cloud Database)    │  │ (Structured JSON Mode)│
                     └──────────────────────┘  └───────────────────────┘
```

### Technology Highlights
- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, Google Generative AI SDK.
- **Database**: Cloud PostgreSQL on Supabase with connection pooling (`pool_pre_ping`), with SQLite support for zero-config offline runs.
- **Authentication**: Salted PBKDF2-HMAC-SHA256 password hashing with user sessions.
- **Frontend**: React 18, Vite, Axios, Lucide Icons, CSS Design Tokens tailored to Node Solutions branding (`#3BC4D9` Cyan, `#0C1116` Dark Slate).
- **Deployment-Ready**: Compatible with Render (Backend) and Vercel (Frontend).

---

## 📁 Repository Structure

```
node-solutions-triage-ai/
├── backend/
│   ├── requirements.txt            # Python dependencies (FastAPI, SQLAlchemy, psycopg2, etc.)
│   └── src/
│       ├── main.py                 # FastAPI application, CORS, table creation & startup seeding
│       ├── settings.py             # Environment configuration & dotenv loader
│       ├── models/
│       │   └── models.py           # Pydantic schemas (TriageRequest, TriageResult, Auth, APIResponse)
│       ├── repositories/
│       │   ├── database.py         # SQLAlchemy engine factory (PostgreSQL / SQLite support)
│       │   ├── repo.py             # TriageRecord repository operations
│       │   ├── user_repo.py        # User authentication & credential verification queries
│       │   └── schema/
│       │       └── schema.py       # SQLAlchemy ORM models (users, triage_records)
│       ├── service/
│       │   └── triage_service.py   # AI pipeline orchestration & prompt integration
│       ├── router/
│       │   └── router.py           # API endpoints (/api/triage, /api/history, /api/auth/*)
│       └── utils/
│           ├── security.py         # Salted PBKDF2 password hashing & verification
│           ├── prompt.py           # Engineered Gemini system prompt with few-shot examples
│           └── response_helper.py  # Standardized API response envelopes
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx                 # App shell with authentication gate
│       ├── index.css               # Design system, CSS variables, components & responsive layout
│       ├── components/
│       │   ├── InputPanel.jsx      # Request submission textarea with char counter & quick examples
│       │   ├── TriageCard.jsx      # Result card with badges, rationale, routing, copyable draft
│       │   ├── HistoryPanel.jsx    # Real-time sidebar history with status tags
│       │   ├── PriorityBadge.jsx   # Dynamic priority chips (Urgent, High, Medium, Low)
│       │   └── CategoryTag.jsx     # Visual category badges
│       ├── pages/
│       │   ├── Dashboard.jsx       # Main application view with user badge & logout
│       │   └── Login.jsx           # Clean authentication screen
│       └── services/
│           └── api.js              # Axios client configured for local and cloud environments
└── README.md
```

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- A Google Gemini API Key

### 2. Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `backend/src/.env`:
   ```ini
   GEMINI_API_KEY=your_gemini_api_key_here
   # Optional: defaults to sqlite:///./triage.db if not provided
   DB_URL=postgresql://postgres:[USERNAME]:[ENCODED_PASSWORD]@[HOST]:5432/postgres
   ```
5. Start the FastAPI server:
   ```bash
   uvicorn main:app --app-dir src --reload --port 8000
   ```
   The backend API will be running at `http://localhost:8000` (Docs available at `http://localhost:8000/docs`).

### 3. Frontend Setup
1. In a new terminal, navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install packages:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open your browser at `http://localhost:5173`.

---

## 🔒 Authentication & Access Control

Access to the Triage Dashboard is protected by a database-backed sign-in gate.
- Passwords are encrypted using **PBKDF2-HMAC-SHA256** with a random salt before being stored in PostgreSQL.
- Sessions persist securely in local state.
- Accounts are provisioned through the backend authentication repository.
- Users can log out at any time using the **Sign Out** button in the dashboard navigation bar.

*(Note: For test accounts or evaluator access credentials, please refer to the private submission email.)*

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/login` | Authenticates user credentials against the database |
| `POST` | `/api/auth/register` | Registers a new authorized user account |
| `POST` | `/api/triage` | Submits raw text to Gemini AI pipeline and saves triage record |
| `GET` | `/api/history` | Retrieves all past triage logs ordered newest first |
| `GET` | `/` | Health check endpoint returning API version |

---

## 🌐 Production Deployment Guide

### Deploying Backend on Render
1. Create a new **Web Service** pointing to your GitHub repository.
2. Set **Root Directory** to `backend`.
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `uvicorn main:app --app-dir src --host 0.0.0.0 --port $PORT`
5. Configure Environment Variables in the Render dashboard:
   - `GEMINI_API_KEY`: Your Gemini API key.
   - `DB_URL`: Your Supabase connection string.
   - `PYTHON_VERSION`: `3.12.0`

### Deploying Frontend on Vercel
1. Import the repository on [Vercel](https://vercel.com).
2. Set **Root Directory** to `frontend`.
3. Add an Environment Variable:
   - `VITE_API_URL`: `https://<your-render-backend-url>.onrender.com`
4. Click **Deploy**.

---

## 📄 License & Attribution
Developed for the **Node Solutions Technical Challenge**. Designed in alignment with Node Solutions brand principles and AI triage specifications.
