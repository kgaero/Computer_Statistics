"""Tests for OneClickSystemMonitor agent callbacks."""

import json
from pathlib import Path
import sys
import types

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "agents"))


def _install_genai_stubs() -> None:
  """Install minimal google.genai stubs for callback imports."""
  google_module = sys.modules.get("google")
  if google_module is None:
    google_module = types.ModuleType("google")

  genai_module = types.ModuleType("google.genai")
  genai_types_module = types.ModuleType("google.genai.types")

  class Part:
    def __init__(self, text: str | None = None) -> None:
      self.text = text

  class Content:
    def __init__(self, parts=None) -> None:
      self.parts = parts or []

  genai_types_module.Part = Part
  genai_types_module.Content = Content
  genai_module.types = genai_types_module
  google_module.genai = genai_module

  sys.modules["google"] = google_module
  sys.modules["google.genai"] = genai_module
  sys.modules["google.genai.types"] = genai_types_module


_install_genai_stubs()

from google.genai import types as genai_types  # noqa: E402
from agents.oneclicksystemmonitor.callbacks import (  # noqa: E402
  log_summary_input_payload,
  only_ram_after_agent_callback,
  skip_agent_if_requested,
)


class DummyCallbackContext:
  """Minimal callback context stub for tests."""

  def __init__(self, text: str | None = None, state=None) -> None:
    if text is None:
      self.user_content = None
    else:
      self.user_content = genai_types.Content(
        parts=[genai_types.Part(text=text)]
      )
    self.state = state or {}


def test_before_agent_callback_skips_on_keyword():
  context = DummyCallbackContext("skip")

  result = skip_agent_if_requested(context)

  assert result is not None
  expected = "Skipping agent execution as requested."
  assert result.parts[0].text == expected


def test_before_agent_callback_no_skip_for_other_text():
  context = DummyCallbackContext("run the report")

  result = skip_agent_if_requested(context)

  assert result is None


def test_after_agent_callback_only_ram_returns_total():
  context = DummyCallbackContext(
    "only RAM",
    state={"memory_stats": {"total_gb": 32}},
  )

  result = only_ram_after_agent_callback(context)

  assert result is not None
  assert result.parts[0].text == "Total RAM: 32 GB"


def test_after_agent_callback_only_ram_handles_missing_stats():
  context = DummyCallbackContext("only ram")

  result = only_ram_after_agent_callback(context)

  assert result is not None
  assert result.parts[0].text == "Total RAM: unavailable."


def test_after_agent_callback_ignores_other_text():
  context = DummyCallbackContext(
    "full report",
    state={"memory_stats": {"total_gb": 16}},
  )

  result = only_ram_after_agent_callback(context)

  assert result is None


def test_log_summary_input_payload_writes_jsonl(monkeypatch):
  log_path = Path("agents/summary_inputs_test.jsonl")
  monkeypatch.setenv("SUMMARY_AGENT_INPUT_LOG_PATH", str(log_path))
  context = DummyCallbackContext(
    "Full report please",
    state={
      "cpu_stats": {"usage_percent": 12.5},
      "api_key": "secret",
    },
  )

  try:
    result = log_summary_input_payload(context)

    assert result is None
    assert log_path.exists()
    payload = json.loads(log_path.read_text(encoding="utf-8").strip())
    assert payload["schema_version"] == "summary-input-v1"
    assert payload["user_request"] == "Full report please"
    assert payload["metrics"]["cpu_stats"]["usage_percent"] == 12.5
    assert payload["state"]["api_key"] == "[REDACTED]"
  finally:
    if log_path.exists():
      log_path.unlink()
