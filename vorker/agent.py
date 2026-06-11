import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .system_prompt import SYSTEM_PROMPT
from .tools import search_tool, fetch_tool

load_dotenv()

agent = Agent(
    name="vorker_swedish_compliance",
    model=LiteLlm(model="nvidia_nim/meta/llama-3.1-70b-instruct"),
    description="Swedish corporate law and tax compliance advisor",
    instruction=SYSTEM_PROMPT,
    tools=[search_tool, fetch_tool],
)

root_agent = agent