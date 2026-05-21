"""
/api/booking — Mock provider dispatch / booking endpoint.
"""
import logging
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.provider import Provider as ProviderModel
from schemas.booking import BookingRequest, BookingResponse

logger = logging.getLogger("ustaadji.booking")

router = APIRouter(prefix="/api", tags=["booking"])


@router.post("/booking", response_model=BookingResponse)
async def create_booking(
    request: BookingRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Finalize / mock the dispatch of a chosen provider.

    In a production system this would create a real booking record,
    send an SMS to the provider, and initiate a payment hold.
    For the hackathon MVP we simulate the confirmation.
    """
    # ── Look up provider ─────────────────────────────────────────────
    result = await db.execute(
        select(ProviderModel).where(ProviderModel.id == request.provider_id)
    )
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(
            status_code=404,
            detail=f"Provider with id {request.provider_id} not found.",
        )

    # ── Generate mock booking ────────────────────────────────────────
    booking_id = f"UJ-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.now()
    eta_min = now + timedelta(minutes=30)
    eta_max = now + timedelta(minutes=60)

    confirmation_msg = (
        f"✅ Booking confirmed! {provider.name} ({provider.category.replace('_', ' ').title()}) "
        f"has been dispatched to your location. "
        f"Expected arrival: {eta_min.strftime('%I:%M %p')} – {eta_max.strftime('%I:%M %p')}. "
        f"Booking reference: {booking_id}. "
        f"Shukriya for using UstaadJi! 🛠️"
    )

    logger.info(
        "Booking %s created — provider=%s (id=%d), user=%s",
        booking_id,
        provider.name,
        provider.id,
        request.user_id,
    )

    return BookingResponse(
        booking_id=booking_id,
        status="confirmed",
        provider_name=provider.name,
        provider_phone=provider.phone,
        provider_category=provider.category,
        message=confirmation_msg,
        estimated_arrival=f"{eta_min.strftime('%I:%M %p')} – {eta_max.strftime('%I:%M %p')}",
        booked_at=now.isoformat(),
    )
