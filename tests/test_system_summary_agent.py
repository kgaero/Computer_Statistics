"""Tests for OneClickSystemMonitor modified components."""

from enum import Enum
from pathlib import Path
import sys
import types

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# --- Stubbing google.adk ---
def _install_google_adk_stubs() -> None:
  """Install minimal google.adk stubs."""
  google_module = types.ModuleType("google")
  adk_module = types.ModuleType("google.adk")
  agents_module = types.ModuleType("google.adk.agents")
  run_config_module = types.ModuleType("google.adk.agents.run_config")
  tools_module = types.ModuleType("google.adk.tools")
  psutil_module = types.ModuleType("psutil")

  class StreamingMode(Enum):
    NONE = "none"

  class RunConfig:
    def __init__(self, **kwargs) -> None:
      self.kwargs = kwargs

  class ToolContext:
    def __init__(self) -> None:
      self.state = {}

  class FunctionTool:
    def __init__(self, func) -> None:
      self.func = func

  class LlmAgent:
    def __init__(self, **kwargs) -> None:
      self.kwargs = kwargs
      self.output_schema = kwargs.get("output_schema")
      self.instruction = kwargs.get("instruction")

  class ParallelAgent:
    def __init__(self, **kwargs) -> None:
      self.kwargs = kwargs

  class SequentialAgent:
    def __init__(self, **kwargs) -> None:
      self.kwargs = kwargs

  class Error(Exception):
    pass

  run_config_module.RunConfig = RunConfig
  run_config_module.StreamingMode = StreamingMode
  agents_module.LlmAgent = LlmAgent
  agents_module.ParallelAgent = ParallelAgent
  agents_module.SequentialAgent = SequentialAgent
  tools_module.ToolContext = ToolContext
  tools_module.FunctionTool = FunctionTool
  psutil_module.Error = Error

  adk_module.agents = agents_module
  adk_module.tools = tools_module
  google_module.adk = adk_module

  sys.modules["google"] = google_module
  sys.modules["google.adk"] = adk_module
  sys.modules["google.adk.agents"] = agents_module
  sys.modules["google.adk.agents.run_config"] = run_config_module
  sys.modules["google.adk.tools"] = tools_module
  sys.modules["psutil"] = psutil_module

_install_google_adk_stubs()

# --- Imports after stubbing ---
from agents.oneclicksystemmonitor.tools import cpu_tools
from agents.oneclicksystemmonitor.sub_agents.summary import agent as summary_agent_module

class DummyPsutilCpu:
  def cpu_percent(self, interval=None, percpu=False):
    return [10.0]
  def process_iter(self, attrs):
    return []
  def sensors_temperatures(self, fahrenheit=False):
    return {}

class SimpleMonkeyPatch:
  def setattr(self, target, name, value):
    self.target = target
    self.name = name
    self.orig = getattr(target, name, None)
    setattr(target, name, value)

  def undo(self):
    if hasattr(self, 'orig') and self.orig is not None:
      setattr(self.target, self.name, self.orig)
    else:
      # If it didn't exist before, maybe we should delete it?
      # But for this test we are replacing a stub module, so we assume it exists.
      pass

def test_collect_cpu_stats_adds_timestamp():
  mp = SimpleMonkeyPatch()
  context = cpu_tools.ToolContext()
  mp.setattr(cpu_tools, "psutil", DummyPsutilCpu())

  try:
      result = cpu_tools.collect_cpu_stats(context)

      assert "timestamp" in context.state
      assert "UTC" in context.state["timestamp"]
      print(f"Timestamp captured: {context.state['timestamp']}")
  finally:
      mp.undo()

def test_summary_agent_configuration():
  agent = summary_agent_module.summary_agent

  # Check if output_schema is set
  assert agent.output_schema is not None
  schema = agent.output_schema

  # Verify schema fields and aliases
  fields = schema.model_fields
  assert "system_performance_summary" in fields
  assert fields["system_performance_summary"].alias == "System Performance Summary"

  assert "total_ram" in fields
  assert fields["total_ram"].alias == "Total RAM"

  # Verify instruction contains references to stats
  instruction = agent.instruction
  assert "{timestamp}" in instruction
  assert "{cpu_stats}" in instruction
  assert "{memory_stats}" in instruction
  assert "{disk_stats}" in instruction

if __name__ == "__main__":
    try:
        test_collect_cpu_stats_adds_timestamp()
        print("test_collect_cpu_stats_adds_timestamp PASSED")
        test_summary_agent_configuration()
        print("test_summary_agent_configuration PASSED")
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
