from dataclasses import dataclass, field
from typing import Literal

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

    def to_bytes(self) -> bytes:
        """Encode HTTP response to bytes"""

        return f"HTTP/1.1 {self.status[0]} {self.status[1]}\r\n{"\r\n".join((f"{key}: {value}" for key, value in self.headers.items()))}\r\n{self.body}".encode()
