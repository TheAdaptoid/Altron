import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """
    Test client fixture for FastAPI application.
    """
    return TestClient(app)
