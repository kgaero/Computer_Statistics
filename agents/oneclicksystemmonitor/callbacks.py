"""Agent callbacks for OneClickSystemMonitor."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from google.genai import types

SKIP_KEYWORD = "skip"
ONLY_RAM_KEYWORD = "only ram"
SKIP_RESPONSE = "Skipping agent execution as requested."
RAM_UNAVAILABLE_RESPONSE = "Total RAM: unavailable."
RAM_RESPONSE_TEMPLATE = "Total RAM: {total_gb} GB"

if TYPE_CHECKING:
  from google.adk.agents.callback_context import CallbackContext


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


def skip_agent_if_requested(
  callback_context: "CallbackContext",
) -> Optional[types.Content]:
  """Skip agent execution when the user explicitly asks to skip."""
  user_text = _normalize_user_text(callback_context.user_content)
  if SKIP_KEYWORD in user_text:
    return types.Content(parts=[types.Part(text=SKIP_RESPONSE)])
  return None


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
