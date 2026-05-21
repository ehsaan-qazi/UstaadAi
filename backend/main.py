"""
UstaadJi — AI Service Orchestrator for the Informal Economy
Main FastAPI application entry point.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-28s  %(levelname)-7s  %(message)s",
)
logger = logging.getLogger("ustaadji")


# ── Lifespan ────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    logger.info("🚀 UstaadJi API starting — %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("🤖 ADK pipeline loaded (model: gemini-2.5-flash via Vertex AI)")
    yield
    logger.info("👋 UstaadJi API shutting down")


# ── App ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Service Orchestrator for the Informal Economy — powered by Google ADK & Gemini",
    lifespan=lifespan,
)

# ── Routers ─────────────────────────────────────────────────────────────
from routers.providers import router as providers_router
from routers.chat import router as chat_router
from routers.booking import router as booking_router

app.include_router(providers_router)
app.include_router(chat_router)
app.include_router(booking_router)

# ── CORS middleware — allow mobile app and web dashboard ────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "message": "UstaadJi API is live! 🚀",
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check with configuration status."""
    return {
        "status": "healthy",
        "gemini_key_configured": bool(settings.GOOGLE_API_KEY),
        "maps_key_configured": bool(settings.GOOGLE_MAPS_API_KEY),
        "model": settings.GEMINI_MODEL,
        "pipeline": "5-agent sequential (intent → discovery → ranking → pricing → responder)",
        "endpoints": ["/api/chat", "/api/booking", "/api/providers"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
