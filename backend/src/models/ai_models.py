from enum import Enum

from pydantic import BaseModel, Field


class AIModelType(str, Enum):
    """Enum for AI model types."""

    CHAT = "chat"
    EMBEDDING = "embedding"


class AIModelStatus(str, Enum):
    """Enum for AI model statuses."""

    LOADED = "loaded"
    UNLOADED = "not-loaded"


class AIModel(BaseModel):
    """AI Model configuration."""

    id: str = Field(..., description="Unique identifier for the AI model.")
    model_type: AIModelType = Field(
        default=AIModelType.CHAT,
        description="Type of the AI model (chat or embedding).",
    )
    status: AIModelStatus = Field(
        default=AIModelStatus.UNLOADED,
        description="Current status of the AI model (loaded or unloaded).",
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
