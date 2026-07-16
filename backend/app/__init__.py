"""
Package entrypoint.

This allows running:
  uvicorn backend.app:app --port 8000
and still serving the FastAPI app.
"""

from .main import app  # noqa: F401

