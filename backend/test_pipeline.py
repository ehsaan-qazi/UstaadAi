import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.pipeline import orchestrator_pipeline
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

async def test_pipeline():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=orchestrator_pipeline,
        app_name="ustaadji_test",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="ustaadji_test",
        user_id="test_user",
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text="My AC is leaking water and not cooling. I live in G-13 Islamabad.")],
    )

    print("Sending message to UstaadJi Pipeline...")
    
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
                    print(part.text, end="", flush=True)
                    
    print("\n\nPipeline execution complete!")

if __name__ == "__main__":
    asyncio.run(test_pipeline())
