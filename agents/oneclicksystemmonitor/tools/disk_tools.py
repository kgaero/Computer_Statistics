"""Disk collection tool for OneClickSystemMonitor."""

import asyncio
from typing import Any

import psutil
from google.adk.tools import ToolContext

from .units import bytes_to_gb, bytes_to_mb

THROUGHPUT_SAMPLE_INTERVAL = 0.1
THROUGHPUT_UNAVAILABLE_REASON = "Disk throughput not supported."
FRAGMENTATION_UNAVAILABLE_REASON = "Disk fragmentation not available."
PARTITION_SKIP_FS_TYPES = {"", "tmpfs", "devtmpfs"}


def _get_drive_usage() -> list[dict[str, Any]]:
  """Collect drive usage details per partition."""
  drives = []
  seen_mounts = set()
  for partition in psutil.disk_partitions(all=False):
    if partition.fstype in PARTITION_SKIP_FS_TYPES:
      continue
    if partition.mountpoint in seen_mounts:
      continue
    seen_mounts.add(partition.mountpoint)

    try:
      usage = psutil.disk_usage(partition.mountpoint)
    except (PermissionError, OSError):
      continue

    drives.append(
      {
        "mount": partition.mountpoint,
        "total_gb": bytes_to_gb(usage.total),
        "free_gb": bytes_to_gb(usage.free),
        "used_percent": round(usage.percent, 2),
      }
    )

  return drives


async def _get_throughput() -> tuple[float | None, float | None, str | None]:
  """Sample disk throughput using io counters."""
  try:
    first = psutil.disk_io_counters()
    if first is None:
      return None, None, THROUGHPUT_UNAVAILABLE_REASON
    await asyncio.sleep(THROUGHPUT_SAMPLE_INTERVAL)
    second = psutil.disk_io_counters()
    if second is None:
      return None, None, THROUGHPUT_UNAVAILABLE_REASON
  except (AttributeError, OSError):
    return None, None, THROUGHPUT_UNAVAILABLE_REASON

  interval = THROUGHPUT_SAMPLE_INTERVAL
  read_mb_s = bytes_to_mb(max(second.read_bytes - first.read_bytes, 0))
  write_mb_s = bytes_to_mb(max(second.write_bytes - first.write_bytes, 0))
  return round(read_mb_s / interval, 2), round(write_mb_s / interval, 2), None


async def collect_disk_stats(tool_context: ToolContext) -> dict[str, Any]:
  """Collect disk statistics using psutil."""
  drives = _get_drive_usage()
  read_mb_s, write_mb_s, throughput_reason = await _get_throughput()

  data = {
    "drives": drives,
    "read_mb_s": read_mb_s,
    "write_mb_s": write_mb_s,
    "throughput_reason": throughput_reason,
    "fragmentation_percent": None,
    "fragmentation_reason": FRAGMENTATION_UNAVAILABLE_REASON,
  }

  tool_context.state["disk_stats"] = data

  return {
    "status": "ok",
    "data": data,
    "error": None,
  }
