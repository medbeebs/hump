type HttpStatus = tuple[int, str]
"""HTTP Status type consists of code and comment"""

OK_200 = 200, "OK"
"""The request succeeded.

The result and meaning of "success" depends on the HTTP method:
- `GET`: The resource has been fetched and transmitted in the message body.
- `HEAD`: Representation headers are included in the response without any message body.
- `PUT` or `PATCH` or `POST`: The resource describing the result of the action is transmitted in the message body.
"""

CREATED_201 = 201, "Created"
"""The request succeeded, and a new resource was created as a result. This is typically the response sent after `POST` requests, or some `PUT`/`PATCH` requests."""

NO_CONTENT_204 = 204, "No Content"
"""There is no content to send for this request, but the headers are useful. The user agent may update its cached headers for this resource with the new ones."""

PARTIAL_206 = 206, "Partial"
"""This response code is used in response to a range request when the client has requested a part or parts of a resource."""

MOVED_PERMANENTLY_301 = 301, "Moved Permanently"
"""The URL of the requested resource has been changed permanently. The new URL is given in the response."""

FOUND_302 = 302, "Found"
"""This response code means that the URI of requested resource has been changed temporarily. Further changes in the URI might be made in the future, so the same URI should be used by the client in future requests."""

NOT_MODIFIED_304 = 304, "Not Modified"
"""This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response."""

TEMPORARY_REDIRECT_307 = 307, "Temporary Redirect"
"""The server sends this response to direct the client to get the requested resource at another URI with the same method that was used in the prior request. This has the same semantics as the 302 Found response code, with the exception that the user agent must not change the HTTP method used: if a POST was used in the first request, a POST must be used in the redirected request."""

PERMANENT_REDIRECT_308 = 308, "Permanent Redirect"
"""This means that the resource is now permanently located at another URI, specified by the `Location` response header. This has the same semantics as the "301 Moved Permanently" HTTP response code, with the exception that the user agent must not change the HTTP method used: if a `POST` was used in the first request, a `POST` must be used in the second request."""

BAD_REQUEST_400 = 400, "Bad Request"
"""The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing)."""

UNAUTHORIZED_401 = 401, "Unauthorized"
"""Although the HTTP standard specifies "unauthorized", semantically this response means "unauthenticated". That is, the client must authenticate itself to get the requested response."""

FORBIDDEN_403 = 403, "Forbidden"
"""The client does not have access rights to the content; that is, it is unauthorized, so the server is refusing to give the requested resource. Unlike "401 Unauthorized", the client's identity is known to the server."""

NOT_FOUND_404 = 404, "Not Found"
"""Resource is missing without indicating if this is temporary or permanent."""

METHOD_NOT_ALLOWED_405 = 405, "Method Not Allowed"
"""The request method is known by the server but is not supported by the target resource. For example, an API may not allow `DELETE` on a resource, or the `TRACE` method entirely."""

NOT_ACCEPTABLE_406 = 406, "Not Acceptable"
"""This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content that conforms to the criteria given by the user agent."""

REQUEST_TIMEOUT_408 = 408, "Request Timeout"
"""This response is sent on an idle connection by some servers, even without any previous request by the client. It means that the server would like to shut down this unused connection. This response is used much more since some browsers use HTTP pre-connection mechanisms to speed up browsing. Some servers may shut down a connection without sending this message."""

GONE_410 = 410, "Gone"
"""This response is sent when the requested content has been permanently deleted from server, with no forwarding address. Clients are expected to remove their caches and links to the resource. The HTTP specification intends this status code to be used for "limited-time, promotional services". APIs should not feel compelled to indicate resources that have been deleted with this status code."""

LENGTH_REQUIRED_411 = 411, "Length Required"
"""Server rejected the request because the `Content-Length` header field is not defined and the server requires it."""

CONTENT_TOO_LARGE_413 = 413, "Content Too Large"
"""The request body is larger than limits defined by server. The server might close the connection or return a `Retry-After` header field."""

URL_TOO_LONG_414 = 414, "URL Too Long"
"""The URI requested by the client is longer than the server is willing to interpret."""

RANGE_NOT_SATISFIABLE_416 = 416, "Range Not Satisfiable"
"""The ranges specified by the `Range` header field in the request cannot be fulfilled. It's possible that the range is outside the size of the target resource's data."""

IM_A_TEAPOT_418 = 418, "Im A Teapot"
"""The server refuses the attempt to brew coffee with a teapot."""

TOO_MANY_REQUESTS_429 = 429, "Too Many Requests"
"""The user has sent too many requests in a given amount of time (rate limiting)."""

INTERNAL_SERVER_ERROR_500 = 500, "Internal Server Error"
"""The server has encountered a situation it does not know how to handle. This error is generic, indicating that the server cannot find a more appropriate `5XX` status code to respond with."""
