from typing import Any, Literal

from requests import Response, request


def http_request(
    method: Literal["GET", "POST", "PATCH", "DELETE"],
    url: str,
    headers: dict[str, str] | None = None,
    json: dict[str, Any] | None = None,
) -> Response:
    """Make an HTTP request and return the response.

    Args:
        method (Literal["GET", "POST", "PATCH", "DELETE"]): The HTTP method to use
        url (str): The URL to send the request to
        headers (dict[str, str] | None): Optional headers to include in the request
        json (dict[str, Any] | None): Optional JSON data to include in the request

    Returns:
        Response: The response object from the request
    """
    headers = headers or {"Content-Type": "application/json"}
    response = request(method=method, url=url, headers=headers, json=json)
    response.raise_for_status()
    return response
