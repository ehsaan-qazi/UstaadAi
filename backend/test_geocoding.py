"""Test Geocoding API with the Maps API key."""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GOOGLE_MAPS_API_KEY")
print(f"Maps API Key prefix: {key[:10]}...")

url = f"https://maps.googleapis.com/maps/api/geocode/json?address=G-13,Islamabad,Pakistan&key={key}"
r = httpx.get(url)
data = r.json()

print(f"Status: {data.get('status')}")
if data.get("status") == "OK":
    for result in data.get("results", [])[:2]:
        loc = result["geometry"]["location"]
        print(f"  Address: {result['formatted_address']}")
        print(f"  Lat: {loc['lat']}, Lng: {loc['lng']}")
    print("\nGeocoding API test PASSED!")
else:
    print(f"Error: {data.get('error_message', 'Unknown error')}")
    print("Geocoding API test FAILED!")
