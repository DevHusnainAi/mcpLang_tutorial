"""Define the configurable parameters for the agent."""

from __future__ import annotations

from typing import Annotated, TypedDict
from langchain_core.runnables import RunnableConfig, ensure_config


class TemplateMetadata(TypedDict):
    kind: str


class FieldMetadata(TypedDict):
    __template_metadata__: TemplateMetadata


class Configuration(TypedDict):
    """The configuration for the agent."""

    model: Annotated[str, FieldMetadata]
    """The model to use for completions"""

    user_id: Annotated[str, FieldMetadata]
    """The user ID for the current session"""

    @classmethod
    def from_runnable_config(cls, config: RunnableConfig | None = None) -> "Configuration":
        """Create configuration from a RunnableConfig."""
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        return cls(
            model=configurable.get("model", "openai/gpt-4"),
            user_id=configurable.get("user_id", "default"),
        )
