#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python WSGI AWS Lambda handler

Inspired by Zappa and Serverless AWS handlers
License: MIT
"""

import base64
import json
import logging
from importlib import import_module
import os
import sys
from .now_handler_helper import NowMangum

if sys.version_info[0] < 3:
    from urllib import urlparse, unquote
else:
    from urllib.parse import urlparse, unquote


# Set up logging
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig()



def handler(app, event_data, context):
    event = json.loads(event_data['body'])
    headers = event.get('headers') or {}
    parsed_url = urlparse(event['path'])

    body = event.get('body', '')
    encoding = event.get('encoding', None)
    scheme = headers.get("X-Forwarded-Proto", "http")
    server_addr = headers.get("Host", None)
    if server_addr is not None:
        if ":" not in server_addr:
            server_port = 80
        else:
            server_port = int(server_addr.split(":")[1])

        server = (server_addr, server_port)
    else:
        server = None  # pragma: no cover
    client_addr = headers.get('x-real-ip',None)
    client = (client_addr, 0)
        
    if encoding == 'base64':
        body = base64.b64decode(body)
    else:
        body = body.encode()
    handler = NowMangum(app)
    return handler(event, context)


def now_handler(event, context):
    wsgi_app_data = os.environ.get('ASGI_APPLICATION').split('.')
    wsgi_module_name = '.'.join(wsgi_app_data[:-1])
    wsgi_app_name = wsgi_app_data[-1]

    wsgi_module = import_module(wsgi_module_name)
    application = getattr(wsgi_module, wsgi_app_name)
    
    return handler(application, event, context)
