"""
UstaadJi — AI Service Orchestrator for the Informal Economy
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Service Orchestrator for the Informal Economy — powered by Google ADK & Gemini",
)

# CORS middleware — allow mobile app and web dashboard
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
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
