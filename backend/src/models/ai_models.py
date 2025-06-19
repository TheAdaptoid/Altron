from enum import Enum

from pydantic import BaseModel, Field


class AIModelType(str, Enum):
    """Enum for AI model types."""

    CHAT = "chat"
    EMBEDDING = "embedding"
    UNDEFINED = "undefined"


class AIModel(BaseModel):
    """AI Model configuration."""

    id: str = Field(..., description="Unique identifier for the AI model.")
    provider: str = Field(
        ..., description="Provider of the AI model (e.g., OpenAI, Ollama)."
    )
    type: AIModelType = Field(
        default=AIModelType.UNDEFINED,
        description="Type of the AI model (chat or embedding).",
    )
    alias: str | None = Field(
        default=None,
        description="Optional alias for the AI model.",
    )


class InferenceParameters(BaseModel):
    """Inference parameters for the AI model."""

    temperature: float = Field(
        default=0.7,
        description="Sampling temperature for the model.",
    )
    top_p: float = Field(
        default=0.9,
        description="Top-p sampling parameter for the model.",
    )
    max_tokens: int = Field(
        default=1000,
        description="Maximum number of tokens to generate.",
    )
