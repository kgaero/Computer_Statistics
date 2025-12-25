"""Summary sub-agent for OneClickSystemMonitor."""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from ...tools import generate_summary_report

SUMMARY_AGENT_INSTRUCTION = (
  "Generate the plain-text system summary by calling the "
  "generate_summary_report tool and return only the report text."
)

summary_agent = LlmAgent(
  name="summary_reporter",
  model="gemma-3-27b-it",
  description="Summarizes system stats into a plain-text report. Always call the generate_summary_report tool to generate the report.",
  instruction=SUMMARY_AGENT_INSTRUCTION,
  tools=[FunctionTool(func=generate_summary_report)],
)
