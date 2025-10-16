import os
from agno.agent import Agent
from agno.models.google import Gemini

def get_hibernating_longer_than_90():
    pass

status_agent = Agent(
    model=Gemini(
        id="gemini-2.0-flash",
        api_key=os.environ.get("GOOGLE_API_KEY"),
    )
)

status_agent.print_response("What is the capital of France?")