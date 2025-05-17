from collections.abc import AsyncGenerator

import pytest
from requests import Response

from src.data_models import CompletionChunk
from src.providers import LMStudio, Provider, RequestData
from tests.statics import LMSTUDIO_MODEL, LMSTUDIO_URL, TEST_MESSAGE_THREAD

POST_ENDPOINT: str = "http://httpbin.org/post"
GET_ENDPOINT: str = "http://httpbin.org/get"
DELAY_ENDPOINT: str = "http://httpbin.org/delay/2"
STREAM_ENDPOINT: str = "http://httpbin.org/stream/10"


class TestHTTPRequest:
    @pytest.mark.asyncio
    async def test_post(self) -> None:
        response: Response = await Provider.http_request_response(
            request_data=RequestData(
                method="POST",
                url=POST_ENDPOINT,
            ),
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get(self) -> None:
        response: Response = await Provider.http_request_response(
            request_data=RequestData(
                method="GET",
                url=GET_ENDPOINT,
            ),
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_invalid_method(self) -> None:
        with pytest.raises(ValueError):
            await Provider.http_request_response(
                request_data=RequestData(
                    method="PUT",
                    url=GET_ENDPOINT,
                )
            )
        with pytest.raises(ValueError):
            await Provider.http_request_response(
                request_data=RequestData(
                    method="DELETE",
                    url=GET_ENDPOINT,
                )
            )
        with pytest.raises(ValueError):
            await Provider.http_request_response(
                request_data=RequestData(
                    method="PATCH",
                    url=GET_ENDPOINT,
                )
            )

    @pytest.mark.asyncio
    async def test_stream(self) -> None:
        response: AsyncGenerator = Provider.http_request_stream(
            request_data=RequestData(
                method="GET",
                url=STREAM_ENDPOINT,
            ),
        )

        assert isinstance(response, AsyncGenerator)
        async for sample in response:
            assert isinstance(sample, bytes)


class TestLMStudio:
    def test_init(self) -> None:
        lmstudio = LMStudio(base_url=LMSTUDIO_URL)
        assert lmstudio.base_url == LMSTUDIO_URL

    @pytest.mark.asyncio
    async def test_completion(self) -> None:
        lmstudio = LMStudio(base_url=LMSTUDIO_URL)

        completion_stream: AsyncGenerator = lmstudio.request_completion(
            model=LMSTUDIO_MODEL, message_thread=TEST_MESSAGE_THREAD
        )

        assert isinstance(completion_stream, AsyncGenerator)
        async for chunk in completion_stream:
            assert isinstance(chunk, CompletionChunk)
