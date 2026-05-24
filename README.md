# 🛠️ UstaadJi Documentation

## 1. Overall Design & Solution
UstaadJi removes the friction of finding reliable local workers (Ustaads). Instead of relying on word-of-mouth or scrolling through endless directories, the user simply states their problem (e.g., *"My AC is leaking water in G-13"*). 
The solution utilizes an autonomous **Agentic Pipeline** to process this request, fetch real-world data, and return a conversational response with a curated, priced recommendation. The frontend provides a premium, responsive chat interface designed specifically for mobile devices.

## 2. Architecture Overview
The system follows a classic decoupled client-server architecture, enhanced by a cloud-native AI integration:
*   **Frontend (Mobile/Web):** A React Native application built with Expo. It provides a native Chat UI and Booking Confirmation screen. Compiled to web using Expo Web and hosted on Vercel.
*   **Backend (REST API):** A FastAPI (Python) server handling business logic, session management, and routing. Hosted on Google Cloud Run (Dockerized).
*   **Database:** SQLite managed via SQLAlchemy, storing 77+ seeded real-world service providers.
*   **AI Engine:** Google Cloud Vertex AI (Gemini 2.5 Flash) orchestrated via the Google Agent Development Kit (ADK).

## 3. Agents Developed
The core logic relies on a `SequentialAgent` pipeline containing 5 specialized Sub-Agents:
1.  **Intent Agent:** Extracts the service category, location, and urgency from bilingual (English/Roman Urdu) user queries.
2.  **Discovery Agent:** Uses Python-based geocoding tools to convert locations to coordinates and queries the database for nearby providers using the mathematical Haversine formula.
3.  **Ranking Agent:** Ranks the discovered providers based on proximity, Google Maps ratings (1-5), and total review volume.
4.  **Pricing Agent:** Analyzes the exact problem to estimate a realistic local market price range in PKR.
5.  **Responder Agent (UstaadJi):** Synthesizes the data into a warm, bilingual, human-like response recommending the best provider.

## 4. Mock / Real APIs Used
*   **Google Maps Places API (Real):** Used during the database seeding phase (`seed.py`) to scrape real mechanics, plumbers, and electricians in Islamabad to populate the local database.
*   **Google Maps Geocoding API (Real):** Used by the Discovery Agent to dynamically convert user-provided location strings (e.g., "F-8 Markaz") into precise Lat/Lng coordinates.
*   **Google Cloud Vertex AI (Real):** The primary LLM engine powering all 5 agents.
*   **`/api/chat` (Custom API):** The primary endpoint the frontend calls to execute the pipeline.
*   **`/api/booking` (Custom Mock API):** A mock endpoint simulating dispatching a provider and generating a booking confirmation with estimated arrival times.

## 5. Integrations Implemented
*   **Application Default Credentials (ADC):** Securely integrated Vertex AI within Google Cloud Run without exposing any JSON Service Account keys.
*   **In-Memory Session Management:** Implemented an `InMemorySessionService` to track multi-turn conversations based on unique `session_id`s, allowing users to chat back-and-forth contextually.
*   **Expo React Navigation:** Integrated seamless screen transitions between the conversational AI view and the dynamic booking confirmation UI.
