import urllib.parse
import http.client
from wsgiref.headers import Headers


class Request:
    def __init__(self, environ) -> None:
        self.environ = environ

    @property
    def args(self):
        query_params = urllib.parse.parse_qs(self.environ["QUERY_STRING"])
        return {k: v[0] for k, v in query_params.items()}


class Response:
    def __init__(
        self, response=None, status=200, charset="utf-8", content_type="text/html"
    ) -> None:
        self.response = [] or response
        self.charset = charset
        self.headers = Headers()
        content_type = f"{content_type}; charset={charset}"
        self.headers.add_header("content-type", content_type)
        self._status = status

    @property
    def status(self):
        status_string = http.client.responses.get(self._status, "Unknown")
        return f"{self._status} {status_string}"

    def __iter__(self):
        for k in self.response:
            if isinstance(k, bytes):
                yield k
            else:
                yield k.encode(self.charset)


def request_response_application(func):
    def application(environ, start_response):
        request = Request(environ)
        response = func(request)
        start_response(response.status, response.headers.items())
        return iter(response)

    return application


@request_response_application
def application(request):
    name = request.args.get("name", "Gaurav")
    return Response([f"<h1>Hi, I am {name}"])
