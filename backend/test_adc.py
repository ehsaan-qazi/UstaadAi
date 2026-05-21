import os, asyncio
from dotenv import load_dotenv
from google import genai
load_dotenv()
async def test():
    try:
        print(f"Using ADC: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
        client = genai.Client(vertexai=True, project=os.getenv('GOOGLE_CLOUD_PROJECT'), location=os.getenv('GOOGLE_CLOUD_LOCATION'))
        response = await client.aio.models.generate_content(
            model='gemini-1.5-flash-001',
            contents='Say UstaadJi is alive!'
        )
        print(f'SUCCESS! {response.text}')
    except Exception as e:
        print(f'Error: {e}')
asyncio.run(test())
