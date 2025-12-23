"""Tests for Arize AX observability configuration."""

from pathlib import Path
import importlib
import sys
import types

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "agents"))


def _install_arize_stubs():
  """Install minimal stubs for Arize and OpenInference."""
  register_calls = []
  instrument_calls = []

  arize_module = types.ModuleType("arize")
  arize_otel_module = types.ModuleType("arize.otel")

  def register(**kwargs):
    register_calls.append(kwargs)
    return "tracer-provider"

  arize_otel_module.register = register
  arize_module.otel = arize_otel_module

  openinference_module = types.ModuleType("openinference")
  instrumentation_module = types.ModuleType("openinference.instrumentation")
  google_adk_module = types.ModuleType(
    "openinference.instrumentation.google_adk"
  )

  class GoogleADKInstrumentor:
    def instrument(self, tracer_provider=None):
      instrument_calls.append(tracer_provider)

  google_adk_module.GoogleADKInstrumentor = GoogleADKInstrumentor
  instrumentation_module.google_adk = google_adk_module
  openinference_module.instrumentation = instrumentation_module

  sys.modules["arize"] = arize_module
  sys.modules["arize.otel"] = arize_otel_module
  sys.modules["openinference"] = openinference_module
  sys.modules["openinference.instrumentation"] = instrumentation_module
  sys.modules["openinference.instrumentation.google_adk"] = google_adk_module

  return register_calls, instrument_calls


def test_configure_arize_ax_skips_without_env(monkeypatch):
  monkeypatch.delenv("ARIZE_SPACE_ID", raising=False)
  monkeypatch.delenv("ARIZE_API_KEY", raising=False)

  observability = importlib.import_module("deployment.observability")
  observability._ARIZE_CONFIGURED = False

  assert observability.configure_arize_ax() is False


def test_configure_arize_ax_registers_when_env_set(monkeypatch):
  register_calls, instrument_calls = _install_arize_stubs()

  monkeypatch.setenv("ARIZE_SPACE_ID", "space-id")
  monkeypatch.setenv("ARIZE_API_KEY", "api-key")
  monkeypatch.setenv("ARIZE_PROJECT_NAME", "monitoring-project")

  observability = importlib.import_module("deployment.observability")
  observability._ARIZE_CONFIGURED = False

  assert observability.configure_arize_ax() is True

  assert register_calls == [
    {
      "space_id": "space-id",
      "api_key": "api-key",
      "project_name": "monitoring-project",
    }
  ]
  assert instrument_calls == ["tracer-provider"]
