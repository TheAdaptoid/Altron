from fastapi import status
from requests import Response


def test_health_check(client):
    """Test the health check endpoint."""
    response: Response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
