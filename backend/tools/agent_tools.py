import os
import httpx
from database import AsyncSessionLocal
from sqlalchemy import select
from models.provider import Provider
import math

MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

async def geocode_address(address: str) -> dict:
    """Converts a human-readable address into latitude and longitude coordinates."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": MAPS_API_KEY}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                location = data["results"][0]["geometry"]["location"]
                return {"latitude": location["lat"], "longitude": location["lng"]}
    return {"latitude": 33.6517, "longitude": 72.9667} # Fallback to G-13 Islamabad

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

async def discover_providers(category: str, latitude: float, longitude: float, radius_km: float = 10.0) -> list:
    """Queries the database to find service providers nearby matching the category."""
    async with AsyncSessionLocal() as db:
        query = select(Provider)
        if category:
            query = query.where(Provider.category == category)
            
        result = await db.execute(query)
        all_providers = result.scalars().all()
        
        nearby = []
        for p in all_providers:
            dist = haversine(latitude, longitude, p.latitude, p.longitude)
            if dist <= radius_km:
                nearby.append({
                    "id": p.id,
                    "name": p.name,
                    "address": p.address,
                    "rating": p.rating,
                    "reviews": p.user_ratings_total,
                    "distance_km": round(dist, 2)
                })
                
        nearby.sort(key=lambda x: x["distance_km"])
        return nearby[:5] # Return top 5 closest
