from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import math

from database import get_db
from models.provider import Provider as ProviderModel
from schemas.provider import Provider as ProviderSchema

router = APIRouter(prefix="/api/providers", tags=["providers"])

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

@router.get("/", response_model=List[ProviderSchema])
async def get_providers(
    category: Optional[str] = None,
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    query = select(ProviderModel)
    if category:
        query = query.where(ProviderModel.category == category)
    query = query.limit(limit)
    
    result = await db.execute(query)
    providers = result.scalars().all()
    return providers

@router.get("/nearby", response_model=List[ProviderSchema])
async def get_nearby_providers(
    lat: float,
    lng: float,
    category: Optional[str] = None,
    radius_km: float = 10.0,
    db: AsyncSession = Depends(get_db)
):
    query = select(ProviderModel)
    if category:
        query = query.where(ProviderModel.category == category)
        
    result = await db.execute(query)
    all_providers = result.scalars().all()
    
    nearby = []
    for p in all_providers:
        dist = haversine(lat, lng, p.latitude, p.longitude)
        if dist <= radius_km:
            nearby.append((p, dist))
            
    # Sort by distance
    nearby.sort(key=lambda x: x[1])
    return [p[0] for p in nearby]

@router.get("/{provider_id}", response_model=ProviderSchema)
async def get_provider(provider_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProviderModel).where(ProviderModel.id == provider_id))
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider
