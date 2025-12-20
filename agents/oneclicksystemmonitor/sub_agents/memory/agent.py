"""Memory statistics sub-agent for OneClickSystemMonitor."""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from ...tools import collect_memory_stats

MEMORY_AGENT_INSTRUCTION = (
  "Collect memory usage information using the collect_memory_stats tool and "
  "return the tool response."
)

memory_agent = LlmAgent(
  name="memory_monitor",
  model="gemma-3-27b-it",
  description="Collects memory usage statistics.",
  instruction=MEMORY_AGENT_INSTRUCTION,
  tools=[FunctionTool(func=collect_memory_stats)],
)
