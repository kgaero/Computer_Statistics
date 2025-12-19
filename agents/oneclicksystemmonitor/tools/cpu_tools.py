"""CPU collection tool for OneClickSystemMonitor."""

from typing import Any

import psutil
from google.adk.tools import ToolContext

CPU_SAMPLE_INTERVAL = 0.1
TEMPERATURE_UNAVAILABLE_REASON = "CPU temperature not supported."
TOP_PROCESS_UNAVAILABLE_REASON = "Top process data unavailable."


class _ProcessSummary:
  """Lightweight process summary."""

  def __init__(self, name: str, cpu_percent: float) -> None:
    self.name = name
    self.cpu_percent = cpu_percent


def _get_top_process() -> _ProcessSummary | None:
  """Return the top CPU process if available."""
  top_process = None
  for process in psutil.process_iter(["name"]):
    try:
      cpu_percent = process.cpu_percent(interval=None)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
      continue

    if top_process is None or cpu_percent > top_process.cpu_percent:
      process_name = process.info.get("name") or "Unknown"
      top_process = _ProcessSummary(process_name, cpu_percent)

  return top_process


def _get_temperature() -> tuple[float | None, str | None]:
  """Return the first available CPU temperature reading."""
  try:
    temps = psutil.sensors_temperatures(fahrenheit=False)
  except (AttributeError, OSError, psutil.Error):
    return None, TEMPERATURE_UNAVAILABLE_REASON
  if not temps:
    return None, TEMPERATURE_UNAVAILABLE_REASON

  for readings in temps.values():
    for reading in readings:
      if reading.current is not None:
        return round(reading.current, 2), None

  return None, TEMPERATURE_UNAVAILABLE_REASON


def collect_cpu_stats(tool_context: ToolContext) -> dict[str, Any]:
  """Collect CPU statistics using psutil."""
  per_core = psutil.cpu_percent(interval=CPU_SAMPLE_INTERVAL, percpu=True)
  overall = round(sum(per_core) / max(len(per_core), 1), 2)

  top_process = _get_top_process()
  top_process_data = None
  top_process_reason = TOP_PROCESS_UNAVAILABLE_REASON
  if top_process:
    top_process_data = {
      "name": top_process.name,
      "cpu_percent": round(top_process.cpu_percent, 2),
    }
    top_process_reason = None

  temperature_c, temperature_reason = _get_temperature()

  data = {
    "usage_percent": overall,
    "per_core_percent": [round(value, 2) for value in per_core],
    "top_process": top_process_data,
    "top_process_reason": top_process_reason,
    "temperature_c": temperature_c,
    "temperature_reason": temperature_reason,
  }

  tool_context.state["cpu_stats"] = data

  return {
    "status": "ok",
    "data": data,
    "error": None,
  }
