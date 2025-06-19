from src.models.ai_models import AIModel
from src.services.lmstudio import LMStudio


def test_get_models() -> None:
    lmstudio = LMStudio()
    models = lmstudio.get_models(limit=2)
    assert models
    assert len(models) == 2
    assert all(isinstance(model, AIModel) for model in models)
    assert all(model.provider == lmstudio.name for model in models)
