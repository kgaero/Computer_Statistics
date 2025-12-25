"""Summary sub-agent for OneClickSystemMonitor."""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from ...callbacks import log_summary_input_payload

# ENDPOINT_ID = "8117895558498091008"
ENDPOINT_ID = "2340903136488587264"

summary_agent = LlmAgent(
  name="summary_reporter",
  model=LiteLlm(
    model=f"vertex_ai/gemini/{ENDPOINT_ID}",
  ),
  description="Calibrates system health severity from stats.",
  instruction=(
    "You are a system health severity calibrator. Read the input "
    "metrics and return JSON with fields: severity (green|yellow|red) "
    "and reason (short sentence)."
  ),
  before_agent_callback=log_summary_input_payload,
  # tools=[FunctionTool(func=generate_summary_report)],
)
