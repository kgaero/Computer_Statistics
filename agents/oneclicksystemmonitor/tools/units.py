"""Unit conversion helpers for system statistics."""

BYTES_IN_GB = 1024 * 1024 * 1024
BYTES_IN_MB = 1024 * 1024
ROUND_DIGITS = 2


def bytes_to_gb(value: float) -> float:
  """Convert bytes to gigabytes with consistent rounding."""
  return round(value / BYTES_IN_GB, ROUND_DIGITS)


def bytes_to_mb(value: float) -> float:
  """Convert bytes to megabytes with consistent rounding."""
  return round(value / BYTES_IN_MB, ROUND_DIGITS)
