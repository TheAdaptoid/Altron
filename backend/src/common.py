from typing import Any, Literal

from requests import Response, request


def http_request(
    method: Literal["GET", "POST", "PATCH", "DELETE"],
    url: str,
    headers: dict[str, str] | None = None,
    json: dict[str, Any] | None = None,
) -> Response:
    """Make an HTTP request and return the response."""
    headers = headers or {"Content-Type": "application/json"}
    response = request(method=method, url=url, headers=headers, json=json)
    response.raise_for_status()
    return response
