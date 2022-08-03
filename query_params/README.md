
## Create a simple wsgi application that takes input from query parameter and display in a HTML Response.

---

```python
from urllib.parse import parse_qs


def application(environ, start_response):
    query_params = parse_qs(environ.get("QUERY_STRING"))
    name = query_params.get("name", ["Gaurav"])[0]
    status = "200 OK"
    start_response(status, [("Content-Type", "text/plain; charset=utf-8")])
    return [(f"<h1>Hello {name} ! </h1>").encode("utf-8")]

```

#### Query parameters are available to us in `QUERY_STRING` from wsgi.

---

#### *command to run*

`uwsgi --http :8000 --wsgi-file main.py`
