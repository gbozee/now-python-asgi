from http.server import BaseHTTPRequestHandler

import base64
import json
import inspect
import typing

import __NOW_HANDLER_FILENAME
__now_variables = dir(__NOW_HANDLER_FILENAME)

def get_server_and_client(event: dict) -> typing.Tuple:  # pragma: no cover
    """
    Parse the server and client for the scope definition, if possible.
    """
    headers = event.get("headers") or {}
    client_addr = headers.get("x-real-ip", None)
    # client_addr = event["requestContext"].get("identity", {}).get("sourceIp", None)
    client = (client_addr, 0)

    server_addr = event["headers"].get("Host", None)

    if server_addr is not None:
        if ":" not in server_addr:
            server_port = 80
        else:
            server_addr, server_port = server_addr.split(":")
            server_port = int(server_port)

        server = (server_addr, server_port)  # type: typing.Any
    else:
        server = None

    return server, client

def format_headers(headers, decode=False):
    keyToList = {}
    for key, value in headers.items():
        if decode:
            key = key.decode()
            value = value.decode()
        if key not in keyToList:
            keyToList[key] = []
        keyToList[key].append(value)
    return keyToList


if 'handler' in __now_variables or 'Handler' in __now_variables:
    base = __NOW_HANDLER_FILENAME.handler if ('handler' in __now_variables) else  __NOW_HANDLER_FILENAME.Handler
    if not issubclass(base, BaseHTTPRequestHandler):
        print('Handler must inherit from BaseHTTPRequestHandler')
        print('See the docs https://zeit.co/docs/v2/deployments/official-builders/python-now-python')
        exit(1)

    print('using HTTP Handler')
    from http.server import HTTPServer
    from urllib.parse import unquote
    import http
    import _thread

    server = HTTPServer(('', 0), base)
    port = server.server_address[1]

    def now_handler(event, context):
        _thread.start_new_thread(server.handle_request, ())

        payload = json.loads(event['body'])
        path = unquote(payload['path'])
        headers = payload['headers']
        method = payload['method']
        encoding = payload.get('encoding')
        body = payload.get('body')

        if (
            (body is not None and len(body) > 0) and
            (encoding is not None and encoding == 'base64')
        ):
            body = base64.b64decode(body)

        request_body = body.encode('utf-8') if isinstance(body, str) else body
        conn = http.client.HTTPConnection('0.0.0.0', port)
        conn.request(method, path, headers=headers, body=request_body)
        res = conn.getresponse()

        return_dict = {
            'statusCode': res.status,
            'headers': format_headers(res.headers),
        }

        data = res.read()

        try:
            return_dict['body'] = data.decode('utf-8')
        except UnicodeDecodeError:
            return_dict['body'] = base64.b64encode(data).decode('utf-8')
            return_dict['encoding'] = 'base64'

        return return_dict

elif 'app' in __now_variables:
    if (
        not inspect.iscoroutinefunction(__NOW_HANDLER_FILENAME.app) and
        not inspect.iscoroutinefunction(__NOW_HANDLER_FILENAME.app.__call__)
    ):
        print('using Web Server Gateway Interface (WSGI)')
        import sys
        from urllib.parse import urlparse, unquote
        from werkzeug._compat import BytesIO
        from werkzeug._compat import string_types
        from werkzeug._compat import to_bytes
        from werkzeug._compat import wsgi_encoding_dance
        from werkzeug.datastructures import Headers
        from werkzeug.wrappers import Response

        def now_handler(event, context):
            payload = json.loads(event['body'])

            headers = Headers(payload.get('headers', {}))

            body = payload.get('body', '')
            if body != '':
                if payload.get('encoding') == 'base64':
                    body = base64.b64decode(body)
            if isinstance(body, string_types):
                body = to_bytes(body, charset='utf-8')

            url = urlparse(unquote(payload['path']))
            query = url.query
            path = url.path

            environ = {
                'CONTENT_LENGTH': str(len(body)),
                'CONTENT_TYPE': headers.get('content-type', ''),
                'PATH_INFO': path,
                'QUERY_STRING': query,
                'REMOTE_ADDR': headers.get(
                    'x-forwarded-for', headers.get(
                        'x-real-ip', payload.get(
                            'true-client-ip', ''))),
                'REQUEST_METHOD': payload['method'],
                'SERVER_NAME': headers.get('host', 'lambda'),
                'SERVER_PORT': headers.get('x-forwarded-port', '80'),
                'SERVER_PROTOCOL': 'HTTP/1.1',
                'event': event,
                'context': context,
                'wsgi.errors': sys.stderr,
                'wsgi.input': BytesIO(body),
                'wsgi.multiprocess': False,
                'wsgi.multithread': False,
                'wsgi.run_once': False,
                'wsgi.url_scheme': headers.get('x-forwarded-proto', 'http'),
                'wsgi.version': (1, 0),
            }

            for key, value in environ.items():
                if isinstance(value, string_types):
                    environ[key] = wsgi_encoding_dance(value)

            for key, value in headers.items():
                key = 'HTTP_' + key.upper().replace('-', '_')
                if key not in ('HTTP_CONTENT_TYPE', 'HTTP_CONTENT_LENGTH'):
                    environ[key] = value

            response = Response.from_app(__NOW_HANDLER_FILENAME.app, environ)

            return_dict = {
                'statusCode': response.status_code,
                'headers': format_headers(response.headers)
            }

            if response.data:
                return_dict['body'] = base64.b64encode(response.data).decode('utf-8')
                return_dict['encoding'] = 'base64'

            return return_dict
    else:
        print('using Asynchronous Server Gateway Interface (ASGI)')
        import base64
        import asyncio
        import enum
        import traceback
        import urllib.parse
        from dataclasses import dataclass, field
        from typing import Any
        import json
        import logging
        from urllib.parse import urlparse, unquote
        from mangum import Mangum
        from mangum.adapter import ASGIHTTPCycle



        class NowMangum(Mangum):
            def handler(self, event: dict, context: dict) -> dict:
                if "method" in event:
                    response = self.handle_http(event, context)
                # else:
                #     response = self.handle_ws(event, context)

                if self.enable_lifespan:
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(self.lifespan.wait_shutdown())

                return response

            def handle_http(self, event: dict, context: dict) -> dict:
                server, client = get_server_and_client(event)
                headers = event.get("headers", {})
                headers_key_value_pairs = [
                    [k.lower().encode(), v.encode()] for k, v in headers.items()
                ]
                parsed_url = urlparse(event["path"])
                query_string = unquote(parsed_url.query)
                scope = {
                    "type": "http",
                    "http_version": "1.1",
                    "method": event["method"],
                    "headers": headers_key_value_pairs,
                    "path": event["path"],
                    "raw_path": None,
                    "root_path": "",
                    "scheme": headers.get("x-forwarded-proto", "https"),
                    "query_string": query_string,
                    "server": server,
                    "client": client,
                    "asgi": {"version": "3.0"},
                }

                encoding = event.get("encoding", None)
                is_binary = event.get("isBase64Encoded", False)
                body = event.get("body") or b""
                if encoding == "base64":
                    body = base64.b64decode(body)
                elif not isinstance(body, bytes):
                    body = body.encode()

                asgi_cycle = ASGIHTTPCycle(scope, is_binary=is_binary, logger=self.logger)
                asgi_cycle.put_message(
                    {"type": "http.request", "body": body, "more_body": False}
                )
                response = asgi_cycle(self.app)
                return response


        def now_handler(event, context):
            payload = json.loads(event['body'])

            handler = NowMangum(__NOW_HANDLER_FILENAME.app)
            return handler(payload, context)

else:
    print('Missing variable `handler` or `app` in file __NOW_HANDLER_FILENAME.py')
    print('See the docs https://zeit.co/docs/v2/deployments/official-builders/python-now-python')
    exit(1)