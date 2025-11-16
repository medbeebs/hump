# Hump

![PyPI - License](https://img.shields.io/pypi/l/hump?style=for-the-badge)
![PyPI - Types](https://img.shields.io/pypi/types/hump?style=for-the-badge)
![PyPI - Version](https://img.shields.io/pypi/v/hump?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hump?style=for-the-badge)

Hump (a defining part of grizzly's neck) is a zero-dependency simple async web server framework for registering request handlers

# Why

- Because dataclasses have smaller overhead than Pydantic models.
- "I understand how something works only if i know how to create it myself"
- Making software from scratch is something that is inherently fun and challenging

# How

1. Python `socket` package provides the means to connect/accept with `AF_INET` (TCP/IP) protocol
2. Create a socket, set it up as non-blocking, bind to `host, port` pair
3. Listen for incoming connections on socket
4. When client connects, accept, create an asyncio task to handle this request further, main return to 3 to accept other clients
5. Parse incoming request into dataclass `Request` model, pass it into registered async handler by `url, method` pair
6. Gather response data/`Response` object, encode to bytes and send it back
7. Close socket and finish task

# Usage example

```python
import asyncio
from hump import Hump, Request

app = Hump("", 8342)

@app.get("/")
async def index(request: Request):
    return "Hello, world!"

asyncio.run(app.serve())
```

And that's it, you can run this example, go to your browser and perform http request to `localhost:8342` to get `Hello, world!` answer.

You can also return another HTTP status code with data attached like this

```python
from hump import Response, statuses

# ... As defined in example usage before

@app.get("/")
async def index(request: Request)
    return Response("Howdy!", statuses.IM_A_TEAPOT)
```

# Limitations

1. HTTP/1.1 only, no HTTPS
2. No automatic headers handling
3. No automatic json response handling, only `str` to `Response` wrapping
