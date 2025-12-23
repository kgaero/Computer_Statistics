"""Memory collection tool for OneClickSystemMonitor."""

from typing import Any

import psutil
from google.adk.tools import ToolContext

from deployment.observability import trace_tool

from .units import bytes_to_gb

CACHE_UNAVAILABLE_REASON = "Cache metric not available on this platform."


@trace_tool()
def collect_memory_stats(tool_context: ToolContext) -> dict[str, Any]:
  """Collect memory statistics using psutil."""
  memory = psutil.virtual_memory()
  swap = psutil.swap_memory()

  cache_gb = None
  cache_reason = CACHE_UNAVAILABLE_REASON
  cached_value = getattr(memory, "cached", None)
  if cached_value is not None:
    cache_gb = bytes_to_gb(cached_value)
    cache_reason = None

  data = {
    "total_gb": bytes_to_gb(memory.total),
    "available_gb": bytes_to_gb(memory.available),
    "available_percent": round(100 - memory.percent, 2),
    "used_percent": round(memory.percent, 2),
    "cache_gb": cache_gb,
    "cache_reason": cache_reason,
    "swap_total_gb": bytes_to_gb(swap.total),
    "swap_used_gb": bytes_to_gb(swap.used),
    "swap_used_percent": round(swap.percent, 2),
  }

  tool_context.state["memory_stats"] = data

  return {
    "status": "ok",
    "data": data,
    "error": None,
  }
