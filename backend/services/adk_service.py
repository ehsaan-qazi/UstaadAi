"""
ADK Session & Runner Dependency — Singleton setup for FastAPI.

This module initialises the ADK InMemorySessionService and Runner exactly
once and exposes helper functions that FastAPI endpoints can call.
"""
import logging
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.pipeline import orchestrator_pipeline

logger = logging.getLogger("ustaadji.adk")

APP_NAME = "ustaadji"

# ── Singletons (created at module import time) ──────────────────────────
_session_service = InMemorySessionService()
_runner = Runner(
    agent=orchestrator_pipeline,
    app_name=APP_NAME,
    session_service=_session_service,
)


def get_session_service() -> InMemorySessionService:
    """Return the shared ADK session service."""
    return _session_service


def get_runner() -> Runner:
    """Return the shared ADK Runner."""
    return _runner
