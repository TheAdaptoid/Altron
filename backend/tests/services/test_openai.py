from src.models.ai_models import AIModel
from src.services.openai import OpenAI


def test_get_models() -> None:
    openai = OpenAI()
    models = openai.get_models(limit=2)
    assert models
    assert len(models) == 2
    assert all(isinstance(model, AIModel) for model in models)
    assert all(model.provider == openai.name for model in models)
