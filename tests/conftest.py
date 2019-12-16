import os
import pytest

# from moto import mock_dynamodb2
# import boto3


@pytest.fixture
def mock_http_now_event(request):
    method = request.param[0]
    body = request.param[1]
    event = {
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
        "method": method,
        "path": "/",
        "body": body,
    }
    return event




@pytest.fixture
def mock_ws_connect_event() -> dict:
    return {
        "headers": {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Host": "test.execute-api.ap-southeast-1.amazonaws.com",
            "Origin": "https://test.execute-api.ap-southeast-1.amazonaws.com",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; " "client_max_window_bits",
            "Sec-WebSocket-Key": "bnfeqmh9SSPr5Sg9DvFIBw==",
            "Sec-WebSocket-Version": "13",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/75.0.3770.100 Safari/537.36",
            "X-Amzn-Trace-Id": "Root=1-5d465cb6-78ddcac1e21f89203d004a89",
            "X-Forwarded-For": "192.168.100.1",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "isBase64Encoded": False,
        "multiValueHeaders": {
            "Accept-Encoding": ["gzip, deflate, br"],
            "Accept-Language": ["en-US,en;q=0.9"],
            "Cache-Control": ["no-cache"],
            "Host": ["test.execute-api.ap-southeast-1.amazonaws.com"],
            "Origin": ["https://test.execute-api.ap-southeast-1.amazonaws.com"],
            "Pragma": ["no-cache"],
            "Sec-WebSocket-Extensions": [
                "permessage-deflate; " "client_max_window_bits"
            ],
            "Sec-WebSocket-Key": ["bnfeqmh9SSPr5Sg9DvFIBw=="],
            "Sec-WebSocket-Version": ["13"],
            "User-Agent": [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X "
                "10_14_5) AppleWebKit/537.36 (KHTML, "
                "like Gecko) Chrome/75.0.3770.100 "
                "Safari/537.36"
            ],
            "X-Amzn-Trace-Id": ["Root=1-5d465cb6-78ddcac1e21f89203d004a89"],
            "X-Forwarded-For": ["192.168.100.1"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"],
        },
        "requestContext": {
            "apiId": "test",
            "connectedAt": 1564892342293,
            "connectionId": "d4NsecoByQ0CH-Q=",
            "domainName": "test.execute-api.ap-southeast-1.amazonaws.com",
            "eventType": "CONNECT",
            "extendedRequestId": "d4NseGc4yQ0FsSA=",
            "identity": {
                "accessKey": None,
                "accountId": None,
                "caller": None,
                "cognitoAuthenticationProvider": None,
                "cognitoAuthenticationType": None,
                "cognitoIdentityId": None,
                "cognitoIdentityPoolId": None,
                "principalOrgId": None,
                "sourceIp": "192.168.100.1",
                "user": None,
                "userAgent": "Mozilla/5.0 (Macintosh; Intel "
                "Mac OS X 10_14_5) "
                "AppleWebKit/537.36 (KHTML, like "
                "Gecko) Chrome/75.0.3770.100 "
                "Safari/537.36",
                "userArn": None,
            },
            "messageDirection": "IN",
            "messageId": None,
            "requestId": "d4NseGc4yQ0FsSA=",
            "requestTime": "04/Aug/2019:04:19:02 +0000",
            "requestTimeEpoch": 1564892342293,
            "routeKey": "$connect",
            "stage": "Prod",
        },
    }


@pytest.fixture
def mock_ws_send_event() -> dict:
    return {
        "body": '{"action": "sendmessage", "data": "Hello world"}',
        "isBase64Encoded": False,
        "requestContext": {
            "apiId": "test",
            "connectedAt": 1564984321285,
            "connectionId": "d4NsecoByQ0CH-Q=",
            "domainName": "test.execute-api.ap-southeast-1.amazonaws.com",
            "eventType": "MESSAGE",
            "extendedRequestId": "d7uRtFvnyQ0FYmw=",
            "identity": {
                "accessKey": None,
                "accountId": None,
                "caller": None,
                "cognitoAuthenticationProvider": None,
                "cognitoAuthenticationType": None,
                "cognitoIdentityId": None,
                "cognitoIdentityPoolId": None,
                "principalOrgId": None,
                "sourceIp": "192.168.100.1",
                "user": None,
                "userAgent": None,
                "userArn": None,
            },
            "messageDirection": "IN",
            "messageId": "d7uRtfaKSQ0CE4Q=",
            "requestId": "d7uRtFvnyQ0FYmw=",
            "requestTime": "05/Aug/2019:05:52:10 +0000",
            "requestTimeEpoch": 1564984330952,
            "routeKey": "sendmessage",
            "stage": "Prod",
        },
    }


@pytest.fixture
def mock_ws_disconnect_event() -> dict:
    return {
        "headers": {
            "Host": "test.execute-api.ap-southeast-1.amazonaws.com",
            "x-api-key": "",
            "x-restapi": "",
        },
        "isBase64Encoded": False,
        "multiValueHeaders": {
            "Host": ["test.execute-api.ap-southeast-1.amazonaws.com"],
            "x-api-key": [""],
            "x-restapi": [""],
        },
        "requestContext": {
            "apiId": "test",
            "connectedAt": 1565140098258,
            "connectionId": "eBqkWf-GSQ0CGmA=",
            "domainName": "test.execute-api.ap-southeast-1.amazonaws.com",
            "eventType": "DISCONNECT",
            "extendedRequestId": "eBql1FJmSQ0FrjA=",
            "identity": {
                "accessKey": None,
                "accountId": None,
                "caller": None,
                "cognitoAuthenticationProvider": None,
                "cognitoAuthenticationType": None,
                "cognitoIdentityId": None,
                "cognitoIdentityPoolId": None,
                "principalOrgId": None,
                "sourceIp": "101.164.35.219",
                "user": None,
                "userAgent": "Mozilla/5.0 (Macintosh; Intel "
                "Mac OS X 10_14_6) "
                "AppleWebKit/537.36 (KHTML, like "
                "Gecko) Chrome/75.0.3770.142 "
                "Safari/537.36",
                "userArn": None,
            },
            "messageDirection": "IN",
            "messageId": None,
            "requestId": "eBql1FJmSQ0FrjA=",
            "requestTime": "07/Aug/2019:01:08:27 +0000",
            "requestTimeEpoch": 1565140107779,
            "routeKey": "$disconnect",
            "stage": "Prod",
        },
    }


# @pytest.fixture(scope="function")
# def dynamodb():
#     with mock_dynamodb2():
#         yield boto3.client("dynamodb", region_name="ap-southeast-1")


def pytest_generate_tests(metafunc):
    os.environ["TABLE_NAME"] = "test-table"
    os.environ["REGION_NAME"] = "ap-southeast-1"
