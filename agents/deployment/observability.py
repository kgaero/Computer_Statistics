"""Arize AX observability setup for OneClickSystemMonitor."""

from __future__ import annotations

import logging
import os
from typing import Any

_DEFAULT_PROJECT_NAME = ""
_LOGGER = logging.getLogger(__name__)
_ARIZE_CONFIGURED = False
_TRACER_PROVIDER = None
_TRACER = None


def configure_arize_ax() -> bool:
  """Configure Arize AX tracing when required env vars are present.

  Returns:
    True when tracing was configured; otherwise False.
  """
  global _ARIZE_CONFIGURED
  if _ARIZE_CONFIGURED:
    return True

  space_id = os.getenv("ARIZE_SPACE_ID")
  api_key = os.getenv("ARIZE_API_KEY")
  if not space_id or not api_key:
    return False

  project_name = os.getenv("ARIZE_PROJECT_NAME", _DEFAULT_PROJECT_NAME)
  endpoint = os.getenv("ARIZE_COLLECTOR_ENDPOINT")

  try:
    from arize.otel import register
    from openinference.instrumentation.google_adk import (
      GoogleADKInstrumentor,
    )
  except ImportError as exc:
    _LOGGER.warning("Arize AX dependencies missing: %s", exc)
    return False

  register_kwargs: dict[str, Any] = {
    "space_id": space_id,
    "api_key": api_key,
    "project_name": project_name,
  }
  if endpoint:
    register_kwargs["endpoint"] = endpoint

  tracer_provider = register(**register_kwargs)
  GoogleADKInstrumentor().instrument(tracer_provider=tracer_provider)
  global _TRACER_PROVIDER
  _TRACER_PROVIDER = tracer_provider
  _ARIZE_CONFIGURED = True
  return True


def _get_tracer():
  """Return the configured tracer when available."""
  if not _ARIZE_CONFIGURED:
    if not configure_arize_ax():
      return None
  global _TRACER
  if _TRACER is not None:
    return _TRACER
  if _TRACER_PROVIDER is None:
    return None
  _TRACER = _TRACER_PROVIDER.get_tracer(__name__)
  return _TRACER


def trace_chain(*args, **kwargs):
  """Return a tracer chain decorator or a no-op decorator."""
  tracer = _get_tracer()
  if tracer is not None and hasattr(tracer, "chain"):
    return tracer.chain(*args, **kwargs)

  def _decorator(func):
    return func

  return _decorator


def trace_tool(*args, **kwargs):
  """Return a tracer tool decorator or a no-op decorator."""
  tracer = _get_tracer()
  if tracer is not None and hasattr(tracer, "tool"):
    return tracer.tool(*args, **kwargs)

  def _decorator(func):
    return func

  return _decorator
