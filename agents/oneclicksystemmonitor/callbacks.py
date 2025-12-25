"""Agent callbacks for OneClickSystemMonitor."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING

from google.genai import types

from deployment.observability import trace_chain

SKIP_KEYWORD = "skip"
ONLY_RAM_KEYWORD = "only ram"
SKIP_RESPONSE = "Skipping agent execution as requested."
RAM_UNAVAILABLE_RESPONSE = "Total RAM: unavailable."
RAM_RESPONSE_TEMPLATE = "Total RAM: {total_gb} GB"
SUMMARY_INPUT_SCHEMA_VERSION = "summary-input-v1"
DEFAULT_SUMMARY_INPUT_LOG_PATH = "agents/summary_agent_inputs.jsonl"
REDACTED_VALUE = "[REDACTED]"
SENSITIVE_KEY_FRAGMENTS = (
  "api_key",
  "apikey",
  "token",
  "secret",
  "password",
  "passwd",
)
_LOGGER = logging.getLogger(__name__)


def _find_repo_root() -> Path:
  """Return the repo root based on AGENTS.md or llms-full.txt."""
  start_path = Path(__file__).resolve()
  for parent in [start_path.parent, *start_path.parents]:
    if (parent / "AGENTS.md").exists() or (parent / "llms-full.txt").exists():
      return parent
  return start_path.parents[2]

if TYPE_CHECKING:
  from google.adk.agents.callback_context import CallbackContext


@trace_chain()
def _normalize_user_text(user_content: Optional[types.Content]) -> str:
  """Return lowercase user text extracted from content parts."""
  if not user_content or not user_content.parts:
    return ""

  text_parts = []
  for part in user_content.parts:
    part_text = getattr(part, "text", None)
    if part_text:
      text_parts.append(part_text)

  return " ".join(text_parts).strip().lower()


@trace_chain()
def _extract_user_text(user_content: Optional[types.Content]) -> str:
  """Return user text extracted from content parts without normalization."""
  if not user_content or not user_content.parts:
    return ""

  text_parts = []
  for part in user_content.parts:
    part_text = getattr(part, "text", None)
    if part_text:
      text_parts.append(part_text)

  return " ".join(text_parts).strip()


@trace_chain()
def _snapshot_state(state: Any) -> dict[str, Any]:
  """Return a shallow snapshot of the session state."""
  if hasattr(state, "to_dict"):
    return state.to_dict()
  if isinstance(state, dict):
    return dict(state)
  return {}


@trace_chain()
def _redact_sensitive(
  value: Any,
  path: list[str],
  redacted: list[str],
) -> Any:
  """Recursively redact likely secrets from payloads."""
  if isinstance(value, dict):
    sanitized: dict[str, Any] = {}
    for key, item in value.items():
      key_text = str(key)
      lowered = key_text.lower()
      if any(fragment in lowered for fragment in SENSITIVE_KEY_FRAGMENTS):
        redacted.append(".".join(path + [key_text]))
        sanitized[key_text] = REDACTED_VALUE
      else:
        sanitized[key_text] = _redact_sensitive(
          item,
          path + [key_text],
          redacted,
        )
    return sanitized

  if isinstance(value, list):
    return [
      _redact_sensitive(item, path + [str(index)], redacted)
      for index, item in enumerate(value)
    ]

  return value


def _resolve_summary_log_path() -> Path:
  """Return the path for summary input JSONL logs."""
  raw_path = os.getenv(
    "SUMMARY_AGENT_INPUT_LOG_PATH",
    DEFAULT_SUMMARY_INPUT_LOG_PATH,
  )
  log_path = Path(raw_path).expanduser()
  repo_root = _find_repo_root()
  if log_path.is_absolute():
    try:
      log_path.relative_to(repo_root)
    except ValueError:
      _LOGGER.warning(
        "Summary log path outside repo; redirecting to repo root."
      )
      return repo_root / log_path.name
    return log_path

  return repo_root / log_path


@trace_chain()
def skip_agent_if_requested(
  callback_context: "CallbackContext",
) -> Optional[types.Content]:
  """Skip agent execution when the user explicitly asks to skip."""
  user_text = _normalize_user_text(callback_context.user_content)
  if SKIP_KEYWORD in user_text:
    return types.Content(parts=[types.Part(text=SKIP_RESPONSE)])
  return None


@trace_chain()
def only_ram_after_agent_callback(
  callback_context: "CallbackContext",
) -> Optional[types.Content]:
  """Replace output with Total RAM when requested by the user."""
  user_text = _normalize_user_text(callback_context.user_content)
  if ONLY_RAM_KEYWORD not in user_text:
    return None

  memory_stats = callback_context.state.get("memory_stats")
  total_gb = None
  if isinstance(memory_stats, dict):
    total_gb = memory_stats.get("total_gb")

  if total_gb is None:
    response_text = RAM_UNAVAILABLE_RESPONSE
  else:
    response_text = RAM_RESPONSE_TEMPLATE.format(total_gb=total_gb)

  return types.Content(parts=[types.Part(text=response_text)])


@trace_chain()
def log_summary_input_payload(
  callback_context: "CallbackContext",
) -> Optional[types.Content]:
  """Persist summary-agent inputs as JSONL for supervised fine-tuning."""
  state = _snapshot_state(getattr(callback_context, "state", {}))
  redacted_fields: list[str] = []
  state_snapshot = _redact_sensitive(state, [], redacted_fields)

  payload = {
    "schema_version": SUMMARY_INPUT_SCHEMA_VERSION,
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "agent": {"name": "summary_reporter"},
    "user_request": _extract_user_text(callback_context.user_content),
    "metrics": {
      "cpu_stats": state_snapshot.get("cpu_stats"),
      "memory_stats": state_snapshot.get("memory_stats"),
      "disk_stats": state_snapshot.get("disk_stats"),
    },
    "context": {
      "host_context": state_snapshot.get("host_context"),
      "app_context": state_snapshot.get("app_context"),
      "recent_incidents": state_snapshot.get("recent_incidents"),
      "user_reports": state_snapshot.get("user_reports"),
    },
    "state": state_snapshot,
    "redacted_fields": redacted_fields,
  }

  log_path = _resolve_summary_log_path()
  log_path.parent.mkdir(parents=True, exist_ok=True)
  with log_path.open("a", encoding="utf-8") as handle:
    handle.write(
      json.dumps(payload, ensure_ascii=True, default=str) + "\n"
    )

  _LOGGER.info("Summary input logged to %s", log_path)

  return None
