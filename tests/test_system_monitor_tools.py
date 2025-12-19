"""Tests for OneClickSystemMonitor tools."""

from enum import Enum
from pathlib import Path
import sys
import types

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))


def _install_google_adk_stubs() -> None:
  """Install minimal google.adk stubs for tool imports."""
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
    pass

  class FunctionTool:
    def __init__(self, func) -> None:
      self.func = func

  class LlmAgent:
    def __init__(self, **kwargs) -> None:
      self.kwargs = kwargs

  class ParallelAgent:
    def __init__(self, **kwargs) -> None:
      self.kwargs = kwargs

  class SequentialAgent:
    def __init__(self, **kwargs) -> None:
      self.kwargs = kwargs

  class Error(Exception):
    """Stub psutil.Error."""

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

from agents.oneclicksystemmonitor.tools import (  # noqa: E402
  collect_cpu_stats,
  collect_memory_stats,
  generate_summary_report,
)
from agents.oneclicksystemmonitor.tools import cpu_tools  # noqa: E402
from agents.oneclicksystemmonitor.tools import memory_tools  # noqa: E402
from agents.oneclicksystemmonitor.tools.units import bytes_to_gb  # noqa: E402


class DummyContext:
  """Minimal tool context stub for tests."""

  def __init__(self) -> None:
    self.state = {}


class DummyVirtualMemory:
  """Stub for psutil.virtual_memory."""

  def __init__(self) -> None:
    self.total = 8 * 1024**3
    self.available = 2 * 1024**3
    self.percent = 75.0
    self.cached = 512 * 1024**2


class DummySwapMemory:
  """Stub for psutil.swap_memory."""

  def __init__(self) -> None:
    self.total = 2 * 1024**3
    self.used = 1 * 1024**3
    self.percent = 50.0


class DummyProcess:
  """Stub for psutil.Process."""

  def __init__(self, name: str, cpu_percent: float) -> None:
    self.info = {"name": name}
    self._cpu_percent = cpu_percent

  def cpu_percent(self, interval: float | None = None) -> float:
    return self._cpu_percent


class DummyPsutilCpu:
  """Stubbed psutil module for CPU tests."""

  class Error(Exception):
    """Stub psutil.Error."""

  class NoSuchProcess(Exception):
    """Stub exception."""

  class AccessDenied(Exception):
    """Stub exception."""

  class ZombieProcess(Exception):
    """Stub exception."""

  def cpu_percent(self, interval: float | None = None, percpu: bool = False):
    if percpu:
      return [10.0, 20.0]
    return 15.0

  def process_iter(self, attrs):
    return [DummyProcess("alpha", 5.0), DummyProcess("beta", 12.5)]

  def sensors_temperatures(self, fahrenheit: bool = False):
    return {}


class DummyPsutilMemory:
  """Stubbed psutil module for memory tests."""

  def virtual_memory(self):
    return DummyVirtualMemory()

  def swap_memory(self):
    return DummySwapMemory()


def test_collect_memory_stats_sets_state(monkeypatch):
  context = DummyContext()
  monkeypatch.setattr(memory_tools, "psutil", DummyPsutilMemory())

  result = collect_memory_stats(context)

  assert result["status"] == "ok"
  assert context.state["memory_stats"]["total_gb"] == bytes_to_gb(
    DummyVirtualMemory().total
  )
  assert context.state["memory_stats"]["swap_used_gb"] == bytes_to_gb(
    DummySwapMemory().used
  )


def test_collect_cpu_stats_handles_missing_temperature(monkeypatch):
  context = DummyContext()
  monkeypatch.setattr(cpu_tools, "psutil", DummyPsutilCpu())

  result = collect_cpu_stats(context)

  cpu_stats = result["data"]
  assert cpu_stats["temperature_c"] is None
  assert cpu_stats["temperature_reason"]
  assert cpu_stats["top_process"]["name"] == "beta"


def test_generate_summary_report_uses_sections():
  context = DummyContext()
  context.state["memory_stats"] = {
    "total_gb": 8,
    "available_gb": 2,
    "available_percent": 25,
    "used_percent": 75,
    "cache_gb": None,
    "cache_reason": "Cache not available.",
    "swap_total_gb": 2,
    "swap_used_gb": 1,
    "swap_used_percent": 50,
  }
  context.state["cpu_stats"] = {
    "usage_percent": 65,
    "per_core_percent": [60, 70],
    "top_process": {"name": "beta", "cpu_percent": 12.5},
    "top_process_reason": None,
    "temperature_c": None,
    "temperature_reason": "CPU temp not available.",
  }
  context.state["disk_stats"] = {
    "drives": [
      {
        "mount": "C:\\",
        "total_gb": 500,
        "free_gb": 90,
        "used_percent": 82,
      }
    ],
    "read_mb_s": None,
    "write_mb_s": None,
    "throughput_reason": "Throughput unavailable.",
    "fragmentation_percent": None,
    "fragmentation_reason": "Fragmentation unavailable.",
  }

  result = generate_summary_report(context)

  report = result["data"]["report"]
  assert "Memory:" in report
  assert "CPU:" in report
  assert "Disk:" in report
  assert "Overall:" in report
