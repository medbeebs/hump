from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

import orjson

from . import __version__
from .statuses import OK_200, HttpStatus

type HttpSafeMethod = Literal["GET", "HEAD", "OPTIONS"]
HTTP_SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
type HttpUnsafeMethod = Literal["POST", "PUT", "PATCH", "DELETE"]
HTTP_UNSAFE_METHODS = ("POST", "PUT", "PATCH", "DELETE")
type HttpMethod = HttpSafeMethod | HttpUnsafeMethod


@dataclass
class Request:
    """HTTP request model representation"""

    method: HttpMethod
    url: str
    headers: dict[str, str]
    body: str

    @classmethod
    def from_bytes(cls, raw_request: bytes):
        """Build Request from constituent parts of connection"""
        request_line, *raw_headers, _spacer, body = raw_request.decode().split("\r\n")

        method, url, _version = request_line.split()
        headers = {
            header[0]: header[1].strip()
            for header in (header.split(":", 1) for header in raw_headers)
            if len(header) == 2
        }

        return cls(method=method, url=url, headers=headers, body=body)


@dataclass
class Response:
    """HTTP Response model representation"""

    body: str = field(default="")
    status: HttpStatus = field(default=OK_200)
    headers: dict[str, str] = field(default_factory=dict)

    def _populate_default_headers(self):
        """Fill out default HTTP Response Headers"""

        self.headers["Date"] = datetime.now(timezone.utc).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )
        self.headers["Server"] = f"Hump {__version__}"

    def to_bytes(self) -> bytes:
        """Encode HTTP response to bytes"""

        self._populate_default_headers()

        body = self.body.encode()
        self.headers["Content-Length"] = len(body)

        return (
            f"HTTP/1.1 {self.status[0]} {self.status[1]}\r\n"
            f"{"\r\n".join((f"{key}: {value}" for key, value in self.headers.items()))}\r\n\r\n".encode()
            + body
        )


@dataclass
class JsonResponse(Response):
    """HTTP JSON Response model representation

    Sets default Content-Type header and uses orjson to dump body"""

    body: Any
    status: HttpStatus = field(default=OK_200)
    headers: dict[str, str] = field(
        default_factory=lambda: {"Content-Type": "application/json"}
    )

    def to_bytes(self) -> bytes:
        """Encode HTTP response to bytes"""

        self._populate_default_headers()

        body = orjson.dumps(self.body)
        self.headers["Content-Length"] = len(body)

        return (
            f"HTTP/1.1 {self.status[0]} {self.status[1]}\r\n"
            f"{"\r\n".join((f"{key}: {value}" for key, value in self.headers.items()))}\r\n\r\n".encode()
            + body
        )
