"""Disk statistics sub-agent for OneClickSystemMonitor."""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from ...tools import collect_disk_stats

DISK_AGENT_INSTRUCTION = (
  "Collect disk usage information using the collect_disk_stats tool and "
  "return the tool response."
)

disk_agent = LlmAgent(
  name="disk_monitor",
  model="gemma-3-27b-it",
  description="Collects disk usage statistics.",
  instruction=DISK_AGENT_INSTRUCTION,
  tools=[FunctionTool(func=collect_disk_stats)],
)
