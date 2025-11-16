import asyncio
import logging
import socket
from types import CoroutineType
from typing import Any

from . import statuses
from .models import HttpMethod, JsonResponse, Request, Response

logger = logging.getLogger(__name__)


class Hump:
    """Async capable web server

    Usage:
    ```python
    import asyncio
    from hump import Hump, Request

    app = Hump("", 8342)

    @app.get("/")
    async def index(request: Request):
        return "Hello, world!"

    asyncio.run(app.serve())
    ```
    """

    def __init__(self, host: str, port: int, backlog=1024, buffer=4096):
        """Create new instance of server"""

        self.bind = (host, port)
        self.backlog = backlog
        self.buffer = buffer

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(False)
        self.server_socket.bind(self.bind)

        self.handlers: dict[tuple[str, HttpMethod], CoroutineType[Any, Any, Any]] = {}

    def get(self, url):
        """Register GET request handler"""

        def wrapper(func):
            self.handlers[(url, "GET")] = func

            return func

        return wrapper

    def head(self, url):
        """Register HEAD request handler"""

        def wrapper(func):
            self.handlers[(url, "HEAD")] = func

            return func

        return wrapper

    def options(self, url):
        """Register OPTIONS request handler"""

        def wrapper(func):
            self.handlers[(url, "OPTIONS")] = func

            return func

        return wrapper

    def post(self, url):
        """Register POST request handler"""

        def wrapper(func):
            self.handlers[(url, "POST")] = func

            return func

        return wrapper

    def put(self, url):
        """Register PUT request handler"""

        def wrapper(func):
            self.handlers[(url, "PUT")] = func

            return func

        return wrapper

    def patch(self, url):
        """Register PATCH request handler"""

        def wrapper(func):
            self.handlers[(url, "PATCH")] = func

            return func

        return wrapper

    def delete(self, url):
        """Register DELETE request handler"""

        def wrapper(func):
            self.handlers[(url, "DELETE")] = func

            return func

        return wrapper

    async def _handle_connection(
        self, conn: socket.SocketType, loop: asyncio.EventLoop
    ):
        """Read data, parse into models and trigger handler"""
        try:
            data = await loop.sock_recv(conn, self.buffer)
            request = Request.from_bytes(data)

            logger.debug(f"Incoming request:\n{request}")

            handler = self.handlers.get((request.url, request.method), None)
            if handler:
                response = await handler(request)
                if not isinstance(response, Response):
                    if isinstance(response, (list, tuple, dict)):
                        response = JsonResponse(response)
                    else:
                        response = Response(response)
            else:
                response = Response("Not Found", statuses.NOT_FOUND_404)

            response_bytes = response.to_bytes()
            logger.debug(f"Outgoing response:\n{response}")

            await loop.sock_sendall(conn, response_bytes)
        finally:
            conn.close()

    async def _listen(self, loop: asyncio.EventLoop):
        """Listen to incoming connections and create asyncio tasks to handle them"""

        logger.info(f"Serving http on host '{self.bind[0]}' port {self.bind[1]}")

        self.server_socket.listen(self.backlog)

        while True:
            conn, addr = await loop.sock_accept(self.server_socket)
            asyncio.create_task(self._handle_connection(conn, loop))

    async def serve(self):
        """Create asyncio event loop and run in it until interrupted"""

        logger.info("Starting Hump")

        loop = asyncio.get_event_loop()
        await self._listen(loop)
