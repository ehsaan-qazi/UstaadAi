"""
Quick ADK verification test — tries multiple auth approaches.
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


async def test_vertexai_adc():
    """Test with Vertex AI using Application Default Credentials (no API key)."""
    from google import genai

    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    print(f"[Vertex AI ADC] Project: {project}, Location: {location}")

    try:
        client = genai.Client(
            vertexai=True,
            project=project,
            location=location,
        )
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents="Say 'UstaadJi is alive!' in one line.",
        )
        print(f"Response: {response.text}")
        print("Vertex AI ADC test PASSED!")
        return "vertexai_adc"
    except Exception as e:
        print(f"Vertex AI ADC test FAILED: {e}\n")
        return None


async def test_api_key_ai_studio():
    """Test with API key via AI Studio endpoint."""
    from google import genai

    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"[AI Studio] Key prefix: {api_key[:10]}...")

    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents="Say 'UstaadJi is alive!' in one line.",
        )
        print(f"Response: {response.text}")
        print("AI Studio API key test PASSED!")
        return "api_key"
    except Exception as e:
        print(f"AI Studio API key test FAILED: {e}\n")
        return None


async def test_vertexai_api_key_header():
    """Test Vertex AI with API key passed as header (workaround)."""
    from google import genai
    from google.genai.types import HttpOptions

    api_key = os.getenv("GOOGLE_API_KEY")
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    print(f"[Vertex AI + API Key Header] Project: {project}")

    try:
        client = genai.Client(
            vertexai=True,
            project=project,
            location=location,
            http_options=HttpOptions(
                api_version="v1",
                headers={"x-goog-api-key": api_key},
            ),
        )
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents="Say 'UstaadJi is alive!' in one line.",
        )
        print(f"Response: {response.text}")
        print("Vertex AI + API Key Header test PASSED!")
        return "vertexai_header"
    except Exception as e:
        print(f"Vertex AI + API Key Header test FAILED: {e}\n")
        return None


async def test_adk_agent(method):
    """Run ADK agent once we know which auth method works."""
    from google.adk.agents import LlmAgent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    print(f"\n--- Testing ADK Agent (auth: {method}) ---")

    agent = LlmAgent(
        name="test_agent",
        model="gemini-2.0-flash",
        instruction="You are a helpful assistant. Respond briefly.",
        description="Test agent for ADK verification.",
    )

    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name="ustaadji_test",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="ustaadji_test",
        user_id="test_user",
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text="Say 'UstaadJi is alive!' in one line.")],
    )

    response_text = ""
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=user_message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text

    print(f"Agent response: {response_text}")
    print("ADK verification PASSED!")


async def main():
    print("=== Testing Gemini API connectivity ===\n")

    # Try approach 1: Vertex AI with API key as header
    method = await test_vertexai_api_key_header()

    # Try approach 2: Vertex AI with ADC
    if not method:
        method = await test_vertexai_adc()

    # Try approach 3: AI Studio with API key
    if not method:
        method = await test_api_key_ai_studio()

    if method:
        await test_adk_agent(method)
    else:
        print("\nAll auth methods failed.")
        print("Please either:")
        print("  1. Install gcloud CLI and run: gcloud auth application-default login")
        print("  2. Or get an API key from https://aistudio.google.com")


if __name__ == "__main__":
    asyncio.run(main())
