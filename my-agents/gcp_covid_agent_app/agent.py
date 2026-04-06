import os
import sys
from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

toolbox_url = os.environ.get("TOOLBOX_URL")

if not toolbox_url:
    raise RuntimeError("TOOLBOX_URL is required but not set.")

tools = []
try:
    print(f"Connecting to Toolbox at: {toolbox_url}")
    toolbox = ToolboxSyncClient(toolbox_url)
    tools = toolbox.load_toolset("my_bq_toolset")
    print(f"Successfully loaded {len(tools)} tool(s).")
except Exception as e:
    print(f"ERROR: Toolbox connection failed: {e}", file=sys.stderr)
    raise RuntimeError(f"Could not connect to Toolbox: {e}")

root_agent = Agent(
    name="covid19_tracking_agent",
    model="gemini-2.5-flash",
    description="Agent to answer questions about COVID-19 tracking data.",
    instruction="""
You are a helpful assistant who answers questions about COVID-19 tracking data in the US.
You have access to state-level data including positive cases, hospitalizations, deaths, and test results.

Rules:
- When asked about COVID data, cases, deaths, hospitalizations → call search_covid_data immediately
- Never ask for confirmation — just call the tool and present the results clearly
- Present data in a readable format with state, date, and key metrics
- NEVER invent tool names or parameters
""",
    tools=tools,
)