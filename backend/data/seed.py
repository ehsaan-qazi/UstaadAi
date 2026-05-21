import asyncio
import os
import random
import httpx
from dotenv import load_dotenv
import sys

# Add parent directory to path to allow importing from database and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, Base, AsyncSessionLocal
from models.provider import Provider

load_dotenv()

MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

CATEGORIES = {
    "plumber": "Plumber in Islamabad",
    "electrician": "Electrician in Islamabad",
    "ac_repair": "AC Repair in Islamabad",
    "carpenter": "Carpenter in Islamabad"
}

# Base coordinates for G-13 Islamabad to generate mock data if needed
BASE_LAT = 33.6517191
BASE_LNG = 72.9667466

MOCK_NAMES = {
    "plumber": ["Ustaad Ali Plumbing", "QuickFix Plumbers", "Islamabad Pipe Experts", "Nawaz Sanitary Store", "Capital Plumbing Services"],
    "electrician": ["Rizwan Electricians", "PowerFix Ustaad", "G-13 Electricals", "Zain Wiring Services", "BrightLight Electricians"],
    "ac_repair": ["CoolTech AC Services", "Ustaad Tariq AC Repair", "ChillBreeze Technicians", "Islamabad HVAC Experts", "Fast AC Fix"],
    "carpenter": ["WoodWorks Ustaad", "Ahmed Carpentry", "Capital Furniture Fix", "G-13 Woodcraft", "Master Carpenters"]
}

async def fetch_real_providers(category: str, query: str):
    print(f"Fetching real data for {category} with query '{query}'...")
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": MAPS_API_KEY
    }
    
    providers = []
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            print(f"Found {len(results)} results for {category}")
            for place in results:
                providers.append({
                    "name": place.get("name", "Unknown"),
                    "category": category,
                    "address": place.get("formatted_address", "Islamabad, Pakistan"),
                    "latitude": place.get("geometry", {}).get("location", {}).get("lat", BASE_LAT),
                    "longitude": place.get("geometry", {}).get("location", {}).get("lng", BASE_LNG),
                    "rating": place.get("rating", round(random.uniform(3.5, 5.0), 1)),
                    "user_ratings_total": place.get("user_ratings_total", random.randint(5, 150)),
                    "is_mock": False
                })
        else:
            print(f"Failed to fetch data for {category}: {response.text}")
            
    return providers

def generate_mock_providers(category: str, count: int):
    print(f"Generating {count} mock providers for {category}...")
    providers = []
    names = MOCK_NAMES.get(category, [f"Mock Provider {i}" for i in range(10)])
    
    for i in range(count):
        # Generate random coordinates around G-13
        lat_offset = random.uniform(-0.05, 0.05)
        lng_offset = random.uniform(-0.05, 0.05)
        name = random.choice(names) + f" (Mock {i})"
        
        providers.append({
            "name": name,
            "category": category,
            "address": "G-13, Islamabad, Pakistan (Mock Address)",
            "latitude": BASE_LAT + lat_offset,
            "longitude": BASE_LNG + lng_offset,
            "rating": round(random.uniform(3.0, 5.0), 1),
            "user_ratings_total": random.randint(1, 200),
            "is_mock": True
        })
        
    return providers

async def main():
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    all_providers = []
    
    for cat, query in CATEGORIES.items():
        real_providers = await fetch_real_providers(cat, query)
        all_providers.extend(real_providers)
        
        # Hybrid approach: If less than 10, fill the gap with mock data
        if len(real_providers) < 10:
            mock_count = 10 - len(real_providers)
            mock_providers = generate_mock_providers(cat, mock_count)
            all_providers.extend(mock_providers)
            
    print(f"Total providers to insert: {len(all_providers)}")
    
    async with AsyncSessionLocal() as session:
        for p_data in all_providers:
            provider = Provider(**p_data)
            session.add(provider)
        await session.commit()
        
    print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(main())
