from fastapi import status
from fastapi.testclient import TestClient
from requests import Response


def test_health_check(client: TestClient) -> None:
    """Test the health check endpoint."""
    response: Response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
