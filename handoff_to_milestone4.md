# UstaadJi Handoff Document (End of Milestone 3)

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

### Milestone 3: Backend API Integration ✅ (Just Completed)
*   **`POST /api/chat`** — Accepts a user message, runs the full 5-agent ADK pipeline, and returns UstaadJi's conversational response. Supports `session_id` for multi-turn conversations.
*   **`POST /api/booking`** — Accepts a `provider_id`, looks up the provider in the DB, and returns a mock dispatch confirmation with booking reference, ETA, and bilingual message.
*   **ADK Session Management** — `InMemorySessionService` is initialized as a singleton (`backend/services/adk_service.py`) and shared across requests. Session continuity verified across multiple requests.
*   **Structured Schemas** — Pydantic v2 schemas created for both endpoints (`backend/schemas/chat.py`, `backend/schemas/booking.py`).
*   **Lifespan logging** — Server logs pipeline readiness on startup.

#### New Files Created in Milestone 3:
| File | Purpose |
|------|---------|
| `backend/routers/chat.py` | `/api/chat` endpoint |
| `backend/routers/booking.py` | `/api/booking` endpoint |
| `backend/services/adk_service.py` | ADK Runner & Session singleton |
| `backend/schemas/chat.py` | Chat request/response schemas |
| `backend/schemas/booking.py` | Booking request/response schemas |

#### API Reference:
```
POST /api/chat
Body: { "message": "My AC is leaking...", "user_id": "user123", "session_id": null }
Returns: { "response": "...", "session_id": "uuid", "user_id": "user123" }

POST /api/booking
Body: { "provider_id": 48, "user_id": "user123" }
Returns: { "booking_id": "UJ-XXXX", "status": "confirmed", "provider_name": "...", ... }

GET /api/health
Returns: pipeline status, configured keys, available endpoints
```

---

## 🚀 What the Next Agent Needs to Do (Milestone 4)
The next step is **Milestone 4: Mobile / Web Frontend Integration**.

**Objectives:**
1.  **Connect the Expo React Native app** (`/mobile`) to the backend `/api/chat` and `/api/booking` endpoints.
2.  **Build a chat UI** that sends messages and displays UstaadJi's responses in a conversational flow.
3.  **Add a booking confirmation screen** that shows provider details and the booking reference.
4.  **Maintain session state** on the client side (store `session_id` from the first response and send it on subsequent requests).

**Crucial Context for the Next Agent:**
*   **API Keys**: The `.env` is fully configured. We are using `gemini-2.5-flash` via Vertex AI (using the Service Account JSON). **DO NOT change the authentication setup.**
*   **To Run Backend**: `cd backend && .\.venv\Scripts\python -m uvicorn main:app --port 8000`
*   **Backend URL**: `http://127.0.0.1:8000`
