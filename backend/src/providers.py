import asyncio
import json
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any

from requests import Response, request
from requests.exceptions import HTTPError

from src.data_models import CompletionChunk, MessageThread, Model

MAX_CONNECTION_RETRIES: int = 5
DEFAULT_CONNECTION_TIMEOUT: int = 60
REQUEST_METHODS: set[str] = {"GET", "POST"}
HTTP_SUCCESS_CODES: set[int] = {200}


@dataclass(slots=True)
class RequestData:
    """Dataclass for request data.

    Attributes:
        method (str): The method of the request.
        url (str): The URL of the request.
        headers (dict[str, str] | None): The headers of the request.
        json (dict | None): The JSON data of the request.
        timeout (int): The timeout of the request.
    """

    method: str
    url: str
    headers: dict[str, str] | None = None
    json: dict[str, Any] | None = None
    timeout: int = DEFAULT_CONNECTION_TIMEOUT

    def __post_init__(self):
        """Post initialization for input validation."""
        if self.method not in REQUEST_METHODS:
            raise ValueError(f"method must be one of {REQUEST_METHODS}")
        if self.headers is None:
            self.headers = {"Content-Type": "application/json"}


class Provider(ABC):
    """Abstract class for inference providers."""

    def __init__(self, base_url: str):
        """A constructor for a Provider."""
        self.base_url = base_url

    @abstractmethod
    async def request_completion(
        self, model: Model, message_thread: MessageThread
    ) -> AsyncGenerator[CompletionChunk, None]:
        """Request a chat completion from the provider."""

    @staticmethod
    async def _http_request(
        request_data: RequestData,
    ) -> Response:
        """Make an HTTP request.

        Args:
            request_data (RequestData): The details of the request.

        Returns:
            Response: The response from the request.
        """
        return request(
            method=request_data.method,
            url=request_data.url,
            headers=request_data.headers,
            json=request_data.json,
            timeout=request_data.timeout,
        )

    @staticmethod
    async def http_request_response(
        request_data: RequestData,
    ) -> Response:
        """Make an HTTP request and expect a normal response.

        Args:
            request_data (RequestData): The details of the request.

        Returns:
            Response: The response from the request.

        Raises:
            Exception: If response status code is not 200.
        """
        event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        response_coroutine = await event_loop.run_in_executor(
            None, Provider._http_request, request_data
        )
        response: Response = await response_coroutine

        if response.status_code not in HTTP_SUCCESS_CODES:
            raise HTTPError(response.status_code, response.text, response=response)

        return response

    @staticmethod
    async def http_request_stream(
        request_data: RequestData,
    ) -> AsyncGenerator[bytes, None]:
        """Make an HTTP request and expect a stream response.

        Args:
            request_data (RequestData): The details of the request.

        Yields:
            Iterator[AsyncGenerator[bytes, None]]: A stream of bytes.
        """
        response: Response = await Provider.http_request_response(request_data)
        for line in response.iter_lines():
            # Ignore empty lines
            if not line:
                continue
            yield line

        # Close the connection
        response.close()


class LMStudio(Provider):
    """A Provider class for LMStudio."""

    def __init__(self, base_url: str):
        """A constructor for LMStudio."""
        super().__init__(base_url=base_url)

    async def request_completion(  # type: ignore
        self, model: Model, message_thread: MessageThread
    ) -> AsyncGenerator[CompletionChunk, None]:
        """Request a chat completion from the provider.

        Args:
            model (Model): The model to use.
            message_thread (MessageThread): The message thread to use.

        Yields:
            Iterator[AsyncGenerator[CompletionChunk, None]]:
                A stream of CompletionChunks.
        """
        # Make the request
        request_data: RequestData = RequestData(
            method="POST",
            url=f"{self.base_url}/v1/chat/completions",
            json={
                "model": model.model_name,
                "messages": message_thread.message_list,
                "stream": True,
            },
        )

        # Stream the response
        response_stream: AsyncGenerator[bytes, None] = LMStudio.http_request_stream(
            request_data
        )

        # Parse the response
        async for chunk_data in response_stream:
            chunk_string: str = chunk_data.decode("utf-8")[6:]
            if chunk_string.startswith("[DONE]"):
                return
            yield CompletionChunk.from_lmstudio_dict(data=json.loads(chunk_string))
