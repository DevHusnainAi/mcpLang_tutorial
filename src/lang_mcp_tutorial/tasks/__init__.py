"""WORKERS AND TASKS.

This module defines tasks which are invoked in the entrypoint.
"""

from src.lang_mcp_tutorial.tasks.workers import call_model

__all__ = ["call_model"]
