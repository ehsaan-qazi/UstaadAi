from google.adk.agents import LlmAgent, SequentialAgent
from tools.agent_tools import geocode_address, discover_providers

# We MUST use gemini-2.5-flash as older models are not available in this Vertex AI environment
MODEL = "gemini-2.5-flash"

# Agent 1: Intent Extraction
intent_agent = LlmAgent(
    name="intent_agent",
    model=MODEL,
    instruction="""You are an intent extractor for home services.
    Analyze the user's message and extract:
    1. The exact service category (MUST be one of: plumber, electrician, ac_repair, carpenter).
    2. The location/address mentioned.
    3. The urgency (high, medium, low).
    Output as JSON ONLY. Example: {"category": "ac_repair", "location": "G-13, Islamabad", "urgency": "high"}""",
    description="Extracts the service category and location from the user's message."
)

# Agent 2: Discovery
discovery_agent = LlmAgent(
    name="discovery_agent",
    model=MODEL,
    instruction="""You are a location and discovery expert.
    1. Look at the JSON output from the previous agent.
    2. Use the 'geocode_address' tool to convert the location string into latitude and longitude.
    3. Use the 'discover_providers' tool with the category and coordinates to find nearby providers.
    4. Return the raw JSON list of the discovered providers.""",
    description="Finds coordinates and discovers local service providers.",
    tools=[geocode_address, discover_providers]
)

# Agent 3: Ranking
ranking_agent = LlmAgent(
    name="ranking_agent",
    model=MODEL,
    instruction="""You are a ranking algorithm.
    Analyze the list of providers found by the discovery agent.
    Rank the top 3 best options based on a combination of:
    - High rating (closer to 5.0 is better)
    - High number of reviews (indicates reliability)
    - Shortest distance_km.
    Present your top 3 ranked providers clearly with reasons.""",
    description="Ranks the discovered providers."
)

# Agent 4: Pricing
pricing_agent = LlmAgent(
    name="pricing_agent",
    model=MODEL,
    instruction="""You are a local pricing expert for Pakistan.
    Based on the service category requested and the user's original issue, provide a fair, realistic estimated market price range in PKR (Pakistani Rupees) for the labor.
    Example: 'AC Gas Refill: 3000 - 5000 PKR'. Keep it brief.""",
    description="Estimates fair market pricing for the service."
)

# Agent 5: Orchestrator / Responder
responder_agent = LlmAgent(
    name="responder_agent",
    model=MODEL,
    instruction="""You are UstaadJi, a friendly and extremely helpful local service coordinator in Pakistan.
    Using the intent, the top 3 ranked providers, and the estimated price from the previous agents:
    1. Write a warm, human-like response to the user.
    2. Recommend the best provider and explain why.
    3. Mention the estimated cost so they aren't surprised.
    4. Ask them politely if they would like to proceed with booking this Ustaad.
    Keep the tone professional yet local (you can sprinkle a little Urdu/Roman Urdu if it feels natural, e.g., 'Ustaad', 'Masla', but keep it highly readable).""",
    description="Drafts the final conversational response to the user."
)

# Wire them together
orchestrator_pipeline = SequentialAgent(
    name="ustaadji_pipeline",
    sub_agents=[intent_agent, discovery_agent, ranking_agent, pricing_agent, responder_agent],
    description="Full pipeline to process a service request, find providers, rank them, estimate price, and respond."
)
