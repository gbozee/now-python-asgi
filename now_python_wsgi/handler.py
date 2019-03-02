#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python WSGI AWS Lambda handler

Inspired by Zappa and Serverless AWS handlers
License: MIT
"""

import base64
import json
import sys
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
from werkzeug._compat import (BytesIO, string_types, to_bytes,
                              wsgi_encoding_dance)


# List of MIME types that should not be base64 encoded. MIME types within
# `text/*` are included by default.
TEXT_MIME_TYPES = [
    'application/json',
    'application/javascript',
    'application/xml',
    'application/vnd.api+json',
    'image/svg+xml',
]


def all_casings(input_string):
    """
    Permute all casings of a given string.
    A pretty algoritm, via @Amber
    http://stackoverflow.com/questions/6792803
    """
    if not input_string:
        yield ""
    else:
        first = input_string[:1]
        if first.lower() == first.upper():
            for sub_casing in all_casings(input_string[1:]):
                yield first + sub_casing
        else:
            for sub_casing in all_casings(input_string[1:]):
                yield first.lower() + sub_casing
                yield first.upper() + sub_casing


def handler(app, lambda_event, context):
    print(lambda_event)
    event = json.loads(lambda_event['body'])
    print(event)

    headers = Headers(event.get('headers', None))

    path_info = event['path']

    body = event.get('body', '')
    if event.get('isBase64Encoded', False):
        body = base64.b64decode(body)
    if isinstance(body, string_types):
        body = to_bytes(body, charset='utf-8')

    environ = {
        'CONTENT_LENGTH': str(len(body)),
        'CONTENT_TYPE': headers.get('Content-Type', ''),
        'PATH_INFO': path_info,
        'REMOTE_ADDR': event.get('x-real-ip', ''),
        'REQUEST_METHOD': event['method'],
        'SERVER_NAME': headers.get('Host', 'lambda'),
        'SERVER_PORT': headers.get('X-Forwarded-Port', '80'),
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'event': lambda_event['body'],
        'wsgi.errors': sys.stderr,
        'wsgi.input': BytesIO(body),
        'wsgi.multiprocess': False,
        'wsgi.multithread': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': headers.get('X-Forwarded-Proto', 'http'),
        'wsgi.version': (1, 0),
    }

    for key, value in environ.items():
        if isinstance(value, string_types):
            environ[key] = wsgi_encoding_dance(value)

    for key, value in headers.items():
        key = 'HTTP_' + key.upper().replace('-', '_')
        if key not in ('HTTP_CONTENT_TYPE', 'HTTP_CONTENT_LENGTH'):
            environ[key] = value

    response = Response.from_app(app, environ)

    # If there are multiple Set-Cookie headers, create case-mutated variations
    # in order to pass them through APIGW. This is a hack that's currently
    # needed. See: https://github.com/logandk/serverless-wsgi/issues/11
    # Source: https://github.com/Miserlou/Zappa/blob/master/zappa/middleware.py
    new_headers = [x for x in response.headers if x[0] != 'Set-Cookie']
    cookie_headers = [x for x in response.headers if x[0] == 'Set-Cookie']
    if len(cookie_headers) > 1:
        for header, new_name in zip(cookie_headers, all_casings('Set-Cookie')):
            new_headers.append((new_name, header[1]))
    elif len(cookie_headers) == 1:
        new_headers.extend(cookie_headers)

    returndict = {
        'statusCode': response.status_code,
        'headers': dict(new_headers)
    }

    if response.data:
        mimetype = response.mimetype or 'text/plain'
        if (
            mimetype.startswith('text/') or mimetype in TEXT_MIME_TYPES
        ) and not response.headers.get('Content-Encoding', ''):
            returndict['body'] = response.get_data(as_text=True)
            returndict['isBase64Encoded'] = False
        else:
            returndict['body'] = base64.b64encode(response.data)\
                                       .decode('utf-8')
            returndict['isBase64Encoded'] = True

    return returndict


def now_handler(event, context):
    from __NOW_HANDLER_FILENAME import application
    return handler(application, event, context)
