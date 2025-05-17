import asyncio
import json
import socket
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from dataclasses import dataclass

from requests import Response, request

from src.data_models import CompletionChunk, MessageThread, Model

MAX_CONNECTION_RETRIES: int = 5
DEFAULT_CONNECTION_TIMEOUT: int = 60
REQUEST_METHODS: set[str] = {"GET", "POST"}


@dataclass(slots=True)
class RequestData:
    method: str
    url: str
    headers: dict[str, str] | None = None
    json: dict | None = None
    timeout: int = DEFAULT_CONNECTION_TIMEOUT

    def __post_init__(self):
        if self.method not in REQUEST_METHODS:
            raise ValueError(f"method must be one of {REQUEST_METHODS}")
        if self.headers is None:
            self.headers = {"Content-Type": "application/json"}


def ping(url: str) -> bool:
    try:
        host, port = url.split(":")
        socket.create_connection((host, int(port)))
        return True
    except OSError:
        return False


class Provider(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def request_completion(
        self, model: Model, message_thread: MessageThread
    ) -> AsyncGenerator[CompletionChunk, None]:
        pass

    @staticmethod
    async def _http_request(
        request_data: RequestData,
    ) -> Response:
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
        event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        response_coroutine = await event_loop.run_in_executor(
            None, Provider._http_request, request_data
        )
        return await response_coroutine

    @staticmethod
    async def http_request_stream(
        request_data: RequestData,
    ) -> AsyncGenerator[bytes, None]:
        response: Response = await Provider.http_request_response(request_data)
        for line in response.iter_lines():
            # Ignore empty lines
            if not line:
                continue
            yield line

        # Close the connection
        response.close()


class LMStudio(Provider):
    def __init__(self, base_url: str):
        super().__init__(base_url=base_url)

    async def request_completion(
        self, model: Model, message_thread: MessageThread
    ) -> AsyncGenerator[CompletionChunk, None]:
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

        response_stream: AsyncGenerator[bytes, None] = LMStudio.http_request_stream(
            request_data
        )

        # Parse the response
        async for chunk_data in response_stream:
            chunk_string: str = chunk_data.decode("utf-8")[6:]
            if chunk_string.startswith("[DONE]"):
                return
            yield CompletionChunk.from_lmstudio_dict(data=json.loads(chunk_string))
