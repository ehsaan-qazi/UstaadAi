"""
/api/chat — REST endpoint that runs the UstaadJi ADK pipeline.
"""
import logging
from fastapi import APIRouter
from google.genai import types

from schemas.chat import ChatRequest, ChatResponse
from services.adk_service import get_session_service, get_runner, APP_NAME

logger = logging.getLogger("ustaadji.chat")

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Accept a natural-language service request, run it through the 5-agent
    pipeline, and return UstaadJi's conversational response.
    """
    session_service = get_session_service()
    runner = get_runner()

    # ── Resolve or create session ────────────────────────────────────
    session_id = request.session_id
    if session_id:
        # Try to resume an existing session
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            session_id=session_id,
        )
        if session is None:
            # ID was provided but not found — create a new one
            logger.warning("Session %s not found; creating new session", session_id)
            session = await session_service.create_session(
                app_name=APP_NAME,
                user_id=request.user_id,
            )
    else:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.user_id,
        )

    # ── Build the ADK Content message ────────────────────────────────
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=request.message)],
    )

    # ── Run the pipeline and collect the final response ──────────────
    response_text = ""
    try:
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session.id,
            new_message=user_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
    except Exception as exc:
        logger.exception("Pipeline error: %s", exc)
        response_text = (
            "Maaf kijiye! UstaadJi ko abhi kuch technical masla ho gaya hai. "
            "Please thori der baad dubara try kijiye. 🙏"
        )

    if not response_text.strip():
        response_text = (
            "UstaadJi is thinking… lekin abhi koi response nahi mila. "
            "Kya aap thora detail se bata sakte hain apna masla?"
        )

    return ChatResponse(
        response=response_text.strip(),
        session_id=session.id,
        user_id=request.user_id,
    )
