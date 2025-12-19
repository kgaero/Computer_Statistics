"""CPU statistics sub-agent for OneClickSystemMonitor."""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from ...tools import collect_cpu_stats

CPU_AGENT_INSTRUCTION = (
  "Collect CPU usage information using the collect_cpu_stats tool and "
  "return the tool response."
)

cpu_agent = LlmAgent(
  name="cpu_monitor",
  model="gemini-2.5-flash",
  description="Collects CPU usage statistics.",
  instruction=CPU_AGENT_INSTRUCTION,
  tools=[FunctionTool(func=collect_cpu_stats)],
)
