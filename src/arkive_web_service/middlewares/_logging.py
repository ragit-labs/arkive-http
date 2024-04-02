import logging
from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, Response
from typing import Callable, Awaitable, List, Tuple, Dict, Any
import json
import uuid
from starlette.types import Scope, Message


class RequestWithBody(Request):
    def __init__(self, scope: Scope, body: bytes):
        super().__init__(scope, self._receive)
        self._body = body
        self._body_returned = False

    async def _receive(self):
        if self._body_returned:
            return {"type": "http.disconnect"}
        else:
            self._body_returned = True
            return {"type": "http.request", "body": self._body, "more_body": False}


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, *, logger: logging.Logger):
        super().__init__(app)
        self._logger = logger

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        request_id: str = str(uuid.uuid4())
        logging_dict: Dict[str, Any] = {"X-API-REQUEST-ID": request_id}

        request_body = await request.body()
        request_headers = dict(request.headers)
        if "authorization" in request_headers:
            del request_headers["authorization"]
        request_quer_params = dict(request.query_params)
        request_path_params = dict(request.path_params)
        new_request = RequestWithBody(request.scope, request_body)

        response = await call_next(new_request)

        response_content_bytes, response_headers, response_status = (
            await self._get_response_params(response)  # type: ignore
        )

        try:
            req_body = json.loads(request_body)
        except json.JSONDecodeError:
            req_body = {}
        logging_dict["request"] = {
            "body": req_body,
            "headers": request_headers,
            "query_params": request_quer_params,
            "path_params": request_path_params,
        }
        logging_dict["response"] = {
            "status_code": response_status,
            "headers": response_headers,
        }
        self._logger.info(logging_dict)
        return Response(response_content_bytes, response_status, response_headers)

    async def _get_response_params(
        self, response: StreamingResponse
    ) -> Tuple[bytes, Dict[str, str], int]:
        """Getting the response parameters of a response and create a new response."""
        response_byte_chunks: List[bytes] = []
        response_status: List[int] = []
        response_headers: List[Dict[str, str]] = []

        async def send(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_status.append(message["status"])
                response_headers.append(
                    {k.decode("utf8"): v.decode("utf8") for k, v in message["headers"]}
                )
            else:
                response_byte_chunks.append(message["body"])

        await response.stream_response(send)  # type: ignore
        content = b"".join(response_byte_chunks)
        return content, response_headers[0], response_status[0]
