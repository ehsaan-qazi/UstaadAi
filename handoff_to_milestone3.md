# UstaadJi Handoff Document (End of Milestone 2)

## 📌 Project Overview
**UstaadJi** is an AI Service Orchestrator for the informal economy (Pakistan focus). It uses Google ADK and Gemini via Vertex AI to understand user requests (e.g., "My AC is leaking"), discover real nearby providers, rank them, estimate pricing, and respond conversationally.

## ✅ What Has Been Completed So Far
### Milestone 0: Setup & Infrastructure
*   Python virtual environment (`backend/.venv`) created with FastAPI, `google-adk`, `google-genai`, `sqlalchemy`, and `aiosqlite`.
*   Mobile app (`/mobile`) initialized with Expo (React Native).

### Milestone 1: Data Layer (Real Data)
*   SQLite Database (`ustaadji.db`) created using SQLAlchemy models (`backend/models/provider.py`).
*   Database was successfully seeded with **77 real-world service providers** (AC Repair, Plumbers, Electricians, Carpenters in Islamabad) fetched directly via the **Google Maps Legacy API**.
*   FastAPI endpoints (`backend/routers/providers.py`) created, including a `/nearby` endpoint utilizing the mathematical Haversine formula to calculate distance based on Lat/Lng.

### Milestone 2: Agent Pipeline (Google ADK)
*   **Authentication Fixed**: The project uses **Vertex AI** via `gemini-2.5-flash`. It authenticates using a Google Cloud Service Account JSON file specified in `.env` under `GOOGLE_APPLICATION_CREDENTIALS`.
*   Created **Tools** (`backend/tools/agent_tools.py`): `geocode_address` and `discover_providers`.
*   Created **5-Agent Pipeline** (`backend/agents/pipeline.py`):
    1.  **Intent Agent**: Extracts category, location, and urgency from messy text.
    2.  **Discovery Agent**: Geocodes location and fetches nearby providers from the DB.
    3.  **Ranking Agent**: Ranks top 3 based on rating, reviews, and distance.
    4.  **Pricing Agent**: Estimates local market labor cost.
    5.  **Responder Agent**: Synthesizes a friendly Roman Urdu/English response.

---

## 🚀 What the Next Agent Needs to Do (Milestone 3)
The next step is **Milestone 3: Backend API Integration**.

**Objectives:**
1.  **Expose the Pipeline**: The 5-Agent pipeline currently only exists in Python code (`test_pipeline.py`). We need to wire it into the FastAPI `main.py` application.
2.  **Create Chat Endpoint**: Create a `POST /api/chat` REST endpoint that accepts a user message string, runs the `SequentialAgent` pipeline using ADK's `Runner`, and returns the final synthesized response string.
3.  **Create Booking Endpoint**: Create a `POST /api/booking` endpoint to finalize/mock the dispatch of the chosen provider.
4.  **Maintain Session State**: Implement ADK's `InMemorySessionService` properly within the FastAPI dependency injection so the user's conversation history is remembered.

**Crucial Context for the Next Agent:**
*   **API Keys**: The `.env` is fully configured. We are using `gemini-2.5-flash` via Vertex AI (using the Service Account JSON). **DO NOT change the authentication setup.**
*   **To Run Backend**: `cd backend && .\venv\Scripts\uvicorn main:app --reload`
*   **To Test Pipeline Locally**: `cd backend && .\venv\Scripts\python test_pipeline.py`
