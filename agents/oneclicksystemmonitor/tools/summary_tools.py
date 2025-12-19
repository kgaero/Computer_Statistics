"""Summary report tool for OneClickSystemMonitor."""

from datetime import datetime, timezone
from typing import Any

from google.adk.tools import ToolContext

HIGH_LOAD_LABEL = "High load"
MODERATE_LOAD_LABEL = "Moderate load"
LOW_LOAD_LABEL = "Low load"

SectionResult = tuple[str, str]
SectionNotesResult = tuple[str, str, list[str]]

MEMORY_HIGH_THRESHOLD = 20
MEMORY_MODERATE_THRESHOLD = 40
CPU_HIGH_THRESHOLD = 80
CPU_MODERATE_THRESHOLD = 50
DISK_HIGH_THRESHOLD = 85
DISK_MODERATE_THRESHOLD = 70


def _format_timestamp() -> str:
  """Return a timezone-aware timestamp string."""
  now = datetime.now(timezone.utc).astimezone()
  return now.strftime("%Y-%m-%d %H:%M %Z")


def _memory_status(available_percent: float) -> tuple[str, str]:
  """Return memory status label and guidance."""
  if available_percent <= MEMORY_HIGH_THRESHOLD:
    return "High usage", "consider closing unused applications."
  if available_percent <= MEMORY_MODERATE_THRESHOLD:
    return "Moderate usage", "monitor large apps for heavy use."
  return "Low usage", "memory usage looks healthy."


def _cpu_status(usage_percent: float) -> tuple[str, str]:
  """Return CPU status label and guidance."""
  if usage_percent >= CPU_HIGH_THRESHOLD:
    return "High usage", "consider closing heavy tasks."
  if usage_percent >= CPU_MODERATE_THRESHOLD:
    return "Moderate usage", "keep an eye on active apps."
  return "Low usage", "CPU load looks healthy."


def _disk_status(drives: list[dict[str, Any]]) -> tuple[str, str]:
  """Return disk status label and guidance."""
  highest_usage = 0
  for drive in drives:
    highest_usage = max(highest_usage, drive.get("used_percent", 0))

  if highest_usage >= DISK_HIGH_THRESHOLD:
    return "High usage", "free up disk space soon."
  if highest_usage >= DISK_MODERATE_THRESHOLD:
    return "Moderate usage", "consider cleaning up unused files."
  return "Low usage", "disk usage looks healthy."


def _overall_status(statuses: list[str]) -> str:
  """Return overall status based on section statuses."""
  if "High" in statuses:
    return HIGH_LOAD_LABEL
  if "Moderate" in statuses:
    return MODERATE_LOAD_LABEL
  return LOW_LOAD_LABEL


def _format_memory_section(memory_stats: dict[str, Any]) -> SectionResult:
  """Render the memory section and return its status label."""
  status_label, guidance = _memory_status(memory_stats["available_percent"])
  lines = [
    "\U0001F9E0 Memory:",
    f"- Total RAM: {memory_stats['total_gb']} GB",
    (
      f"- Available: {memory_stats['available_gb']} GB "
      f"({memory_stats['available_percent']}%)"
    ),
    f"- Status: {status_label} – {guidance}",
  ]
  return "\n".join(lines), status_label


def _format_cpu_section(cpu_stats: dict[str, Any]) -> SectionNotesResult:
  """Render the CPU section and return its status and notes."""
  status_label, guidance = _cpu_status(cpu_stats["usage_percent"])
  notes = []

  top_process_line = "- Top process: Not available"
  if cpu_stats.get("top_process"):
    process = cpu_stats["top_process"]
    top_process_line = (
      f"- Top process: {process['name']} "
      f"({process['cpu_percent']}%)"
    )
  elif cpu_stats.get("top_process_reason"):
    notes.append(cpu_stats["top_process_reason"])

  temperature_line = "- CPU temperature: Not available"
  if cpu_stats.get("temperature_c") is not None:
    temperature_line = (
      f"- CPU temperature: {cpu_stats['temperature_c']} °C"
    )
  elif cpu_stats.get("temperature_reason"):
    notes.append(cpu_stats["temperature_reason"])

  per_core = cpu_stats.get("per_core_percent", [])
  highest_core = max(per_core) if per_core else 0

  lines = [
    "\u2699\ufe0f CPU:",
    f"- Current usage: {cpu_stats['usage_percent']}%",
    f"- Highest core: {round(highest_core, 2)}%",
    top_process_line,
    temperature_line,
    f"- Status: {status_label} – {guidance}",
  ]
  return "\n".join(lines), status_label, notes


def _format_disk_section(disk_stats: dict[str, Any]) -> SectionNotesResult:
  """Render the disk section and return its status and notes."""
  drives = disk_stats.get("drives", [])
  status_label, guidance = _disk_status(drives)
  notes = []

  drive_lines = []
  for drive in drives:
    drive_lines.append(
      (
        f"- {drive['mount']}: {drive['used_percent']}% used "
        f"({drive['free_gb']} GB free of {drive['total_gb']} GB)"
      )
    )

  if not drive_lines:
    drive_lines.append("- No drive usage data available.")

  throughput_line = "- Read/Write: Not available"
  if disk_stats.get("read_mb_s") is not None:
    throughput_line = (
      f"- Read/Write: {disk_stats['read_mb_s']} MB/s / "
      f"{disk_stats['write_mb_s']} MB/s"
    )
  elif disk_stats.get("throughput_reason"):
    notes.append(disk_stats["throughput_reason"])

  fragmentation_note = disk_stats.get("fragmentation_reason")
  if fragmentation_note:
    notes.append(fragmentation_note)

  lines = [
    "\U0001F4BE Disk:",
    *drive_lines,
    throughput_line,
    f"- Status: {status_label} – {guidance}",
  ]
  return "\n".join(lines), status_label, notes


def generate_summary_report(tool_context: ToolContext) -> dict[str, Any]:
  """Generate a plain-text summary report using collected stats."""
  memory_stats = tool_context.state.get("memory_stats")
  cpu_stats = tool_context.state.get("cpu_stats")
  disk_stats = tool_context.state.get("disk_stats")

  missing_sections = []
  notes = []
  status_labels = []

  sections = []
  if memory_stats:
    section, status_label = _format_memory_section(memory_stats)
    sections.append(section)
    status_labels.append(status_label)
  else:
    missing_sections.append("Memory stats unavailable.")

  if cpu_stats:
    section, status_label, cpu_notes = _format_cpu_section(cpu_stats)
    sections.append(section)
    status_labels.append(status_label)
    notes.extend(cpu_notes)
  else:
    missing_sections.append("CPU stats unavailable.")

  if disk_stats:
    section, status_label, disk_notes = _format_disk_section(disk_stats)
    sections.append(section)
    status_labels.append(status_label)
    notes.extend(disk_notes)
  else:
    missing_sections.append("Disk stats unavailable.")

  notes.extend(missing_sections)

  overall_status = _overall_status(status_labels)

  report_lines = [
    f"System Performance Summary (as of {_format_timestamp()}):",
    "",
    *sections,
    "",
    f"\U0001F50E Overall: {overall_status}.",
  ]

  if notes:
    report_lines.extend(["", "Notes:", *[f"- {note}" for note in notes]])

  report = "\n".join(report_lines)

  tool_context.state["summary_report"] = report

  return {
    "status": "ok",
    "data": {
      "report": report,
    },
    "error": None,
  }
