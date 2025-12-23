"""Arize AX observability setup for OneClickSystemMonitor."""

from __future__ import annotations

import logging
import os
from typing import Any

_DEFAULT_PROJECT_NAME = ""
_LOGGER = logging.getLogger(__name__)
_ARIZE_CONFIGURED = False


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
  _ARIZE_CONFIGURED = True
  return True
