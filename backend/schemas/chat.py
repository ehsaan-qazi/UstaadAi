"""
Pydantic schemas for the /api/chat endpoint.
"""
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Incoming user message to the UstaadJi pipeline."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's service request in natural language")
    session_id: Optional[str] = Field(None, description="Existing session ID to continue a conversation")
    user_id: str = Field(default="anonymous", description="Unique user identifier")


class ChatResponse(BaseModel):
    """Response from the UstaadJi pipeline."""
    response: str = Field(..., description="AI-generated response from UstaadJi")
    session_id: str = Field(..., description="Session ID for continuing the conversation")
    user_id: str = Field(..., description="User identifier used for this request")
