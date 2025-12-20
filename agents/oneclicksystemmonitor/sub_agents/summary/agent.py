"""Summary sub-agent for OneClickSystemMonitor."""

from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

SUMMARY_AGENT_INSTRUCTION = """
You are a system monitor assistant. Your task is to generate a structured system performance summary based on the provided statistics.

Data provided:
Timestamp: {timestamp}
Memory Stats: {memory_stats}
CPU Stats: {cpu_stats}
Disk Stats: {disk_stats}

Output a JSON object matching the SystemSummary schema.

Field logic:
- "System Performance Summary": Use the provided Timestamp.
- "Total RAM": Format as "{total_gb} GB" from memory_stats.
- "Available": Format as "{available_gb} GB ({available_percent}%)" from memory_stats.
- "Memory Status": Determine based on memory_stats available_percent:
  - <= 20%: "High usage – consider closing unused applications."
  - <= 40%: "Moderate usage – monitor large apps for heavy use."
  - > 40%: "Low usage – memory usage looks healthy."
- "Current usage": Format as "{usage_percent}%" from cpu_stats.
- "Highest core": Find max of cpu_stats per_core_percent, format as "{max_core}%".
- "Top process": From cpu_stats top_process. If available: "{name} ({cpu_percent}%)". If unavailable (None): "systemd (0.0%)" or "Not available".
- "CPU Status": Determine based on cpu_stats usage_percent:
  - >= 80%: "High usage – consider closing heavy tasks."
  - >= 50%: "Moderate usage – keep an eye on active apps."
  - < 50%: "Low usage – CPU load looks healthy."
- "Read/Write": From disk_stats. If read_mb_s and write_mb_s are available: "{read_mb_s} MB/s / {write_mb_s} MB/s". Else: "0.0 MB/s / 0.0 MB/s" or "Not available".
- "Disk Status": Determine based on highest used_percent of any drive in disk_stats drives:
  - >= 85%: "High usage – free up disk space soon."
  - >= 70%: "Moderate usage – consider cleaning up unused files."
  - < 70%: "Low usage – disk usage looks healthy."
"""


class SystemSummary(BaseModel):
  """Structured system performance summary."""

  system_performance_summary: str = Field(
    alias="System Performance Summary",
    description="The timestamp of the report.",
  )
  total_ram: str = Field(alias="Total RAM")
  available: str = Field(alias="Available")
  memory_status: str = Field(alias="Memory Status")
  current_usage: str = Field(alias="Current usage")
  highest_core: str = Field(alias="Highest core")
  top_process: str = Field(alias="Top process")
  cpu_status: str = Field(alias="CPU Status")
  read_write: str = Field(alias="Read/Write")
  disk_status: str = Field(alias="Disk Status")


summary_agent = LlmAgent(
  name="summary_reporter",
  model="gemma-3-27b-it",
  description="Summarizes system stats into a structured JSON report.",
  instruction=SUMMARY_AGENT_INSTRUCTION,
  output_schema=SystemSummary,
)
