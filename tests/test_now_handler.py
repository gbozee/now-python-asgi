import base64
import json
import os

import pytest
from now_python_asgi import NowMangum, handler
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.templating import Jinja2Templates

# BASE_DIR = os.path.abspath('tests')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
get_request_event = {
    "Action": "Invoke",
    "body": json.dumps(
        {
            "headers": {
                "accept": (
                    "text/html,application/xhtml+xml,application/xml;"
                    "q=0.9,image/webp,image/apng,*/*;q=0.8"
                ),
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "connection": "close",
                "host": "python-wsgi-test.now.sh",
                "internal-lambda-name": "insecure-lambda-name",
                "internal-lambda-region": "iad1",
                "referer": "https://zeit.co/",
                "upgrade-insecure-requests": "1",
                "user-agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X "
                    "10_14_3) AppleWebKit/537.36 (KHTML, "
                    "like Gecko) Chrome/72.0.3626.119 "
                    "Safari/537.36"
                ),
                "x-forwarded-for": "255.255.255.255",
                "x-forwarded-host": "python-wsgi-test.now.sh",
                "x-forwarded-proto": "https",
                "x-now-deployment-url": "python-wsgi-test.now.sh",
                "x-now-id": "insecure-now-id",
                "x-now-log-id": "insecure-now-log-id",
                "x-now-trace": "iad1",
                "x-real-ip": "255.255.255.255",
                "x-zeit-co-forwarded-for": "255.255.255.255",
            },
            "host": "python-wsgi-test.now.sh",
            "method": "GET",
            "path": "/",
        }
    ),
}


def test_now_handler_get_request():
    application = Starlette()

    @application.route("/")
    def homepage(request):
        return PlainTextResponse("Success!")

    response = handler(application, get_request_event, None)
    assert response["statusCode"] == 200
    assert "headers" in response


def test_now_handler_for_jinja_responses():
    templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "tests", "templates"))
    application = Starlette(debug=True)

    @application.route("/")
    async def homepage(request):
        template = "index.html"
        context = {"request": request, "data": "John"}
        return templates.TemplateResponse(template, context)

    response = handler(application, get_request_event, None)
    assert response["statusCode"] == 200
    assert "headers" in response


# @pytest.mark.parametrize("mock_http_now_event", [["GET", None]], indirect=True)
# def test_http_response(mock_http_now_event) -> None:
#     async def app(scope, receive, send):
#         assert scope == {
#             "type": "http",
#             "http_version": "1.1",
#             "method": "GET",
#             "headers": [
#                 [
#                     b"accept",
#                     b"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#                 ],
#                 [b"accept-encoding", b"gzip, deflate, br"],
#                 [b"accept-language", b"en-US,en;q=0.9"],
#                 [b"connection", b"close"],
#                 [b"host", b"python-wsgi-test.now.sh"],
#                 [b"internal-lambda-name", b"insecure-lambda-name"],
#                 [b"internal-lambda-region", b"iad1"],
#                 [b"referer", b"https://zeit.co/"],
#                 [b"upgrade-insecure-requests", b"1"],
#                 [
#                     b"user-agent",
#                     b"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
#                 ],
#                 [b"x-forwarded-for", b"255.255.255.255"],
#                 [b"x-forwarded-host", b"python-wsgi-test.now.sh"],
#                 [b"x-forwarded-proto", b"https"],
#                 [b"x-now-deployment-url", b"python-wsgi-test.now.sh"],
#                 [b"x-now-id", b"insecure-now-id"],
#                 [b"x-now-log-id", b"insecure-now-log-id"],
#                 [b"x-now-trace", b"iad1"],
#                 [b"x-real-ip", b"255.255.255.255"],
#                 [b"x-zeit-co-forwarded-for", b"255.255.255.255"],
#             ],
#             "path": "/",
#             "raw_path": None,
#             "root_path": "",
#             "scheme": "https",
#             "query_string": "",
#             "server": None,
#             "client": ("255.255.255.255", 0),
#             "asgi": {"version": "3.0"},
#         }
#         await send(
#             {
#                 "type": "http.response.start",
#                 "status": 200,
#                 "headers": [[b"content-type", b"text/plain; charset=utf-8"]],
#             }
#         )
#         await send({"type": "http.response.body", "body": b"Hello, world!"})

#     response = handler(
#         app, {"Action": "Invoke", "body": json.dumps(mock_http_now_event)}, None
#     )
#     assert response == {
#         "statusCode": 200,
#         "isBase64Encoded": False,
#         "headers": {"content-type": "text/plain; charset=utf-8"},
#         "body": "Hello, world!",
#     }


@pytest.mark.parametrize("mock_http_now_event", [["GET", None]], indirect=True)
def test_starlette_response(mock_http_now_event) -> None:
    startup_complete = False
    shutdown_complete = False
    path = mock_http_now_event["path"]
    app = Starlette()

    @app.on_event("startup")
    async def on_startup():
        nonlocal startup_complete
        startup_complete = True

    @app.on_event("shutdown")
    async def on_shutdown():
        nonlocal shutdown_complete
        shutdown_complete = True

    @app.route(path)
    def homepage(request):
        return PlainTextResponse("Hello, world!")

    assert not startup_complete
    assert not shutdown_complete

    handler = NowMangum(app)
    mock_http_now_event["body"] = None

    assert startup_complete
    assert not shutdown_complete

    response = handler(mock_http_now_event, {})
    # response = handler(
    #     app, {"Action": "Invoke", "body": json.dumps(mock_http_now_event)}, None
    # )
    assert response == {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {
            "content-length": "13",
            "content-type": "text/plain; charset=utf-8",
        },
        "body": "Hello, world!",
    }
    assert startup_complete
    assert shutdown_complete
