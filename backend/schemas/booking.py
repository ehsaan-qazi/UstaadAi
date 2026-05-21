"""
Pydantic schemas for the /api/booking endpoint.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookingRequest(BaseModel):
    """Request to book/dispatch a provider."""
    provider_id: int = Field(..., description="ID of the chosen provider from the database")
    user_id: str = Field(default="anonymous", description="Unique user identifier")
    service_description: Optional[str] = Field(None, description="Brief description of the service needed")
    session_id: Optional[str] = Field(None, description="Chat session ID that led to this booking")


class BookingResponse(BaseModel):
    """Mock booking confirmation."""
    booking_id: str = Field(..., description="Unique booking reference number")
    status: str = Field(..., description="Booking status (confirmed, pending, failed)")
    provider_name: str = Field(..., description="Name of the dispatched provider")
    provider_phone: Optional[str] = Field(None, description="Provider's contact number")
    provider_category: str = Field(..., description="Service category")
    message: str = Field(..., description="Human-readable confirmation message")
    estimated_arrival: str = Field(..., description="Estimated arrival window")
    booked_at: str = Field(..., description="Timestamp of the booking")
