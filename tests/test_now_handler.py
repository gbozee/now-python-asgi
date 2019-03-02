import json

from werkzeug.wrappers import Request, Response

from now_python_wsgi import handler


get_request_event = {
    'Action': 'Invoke',
    'body': json.dumps({
        'headers': {
            'accept': ('text/html,application/xhtml+xml,application/xml;'
                       'q=0.9,image/webp,image/apng,*/*;q=0.8'),
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'connection': 'close',
            'host': 'python-wsgi-test.now.sh',
            'internal-lambda-name': 'insecure-lambda-name',
            'internal-lambda-region': 'iad1',
            'referer': 'https://zeit.co/',
            'upgrade-insecure-requests': '1',
            'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X '
                           '10_14_3) AppleWebKit/537.36 (KHTML, '
                           'like Gecko) Chrome/72.0.3626.119 '
                           'Safari/537.36'),
            'x-forwarded-for': '255.255.255.255',
            'x-forwarded-host': 'python-wsgi-test.now.sh',
            'x-forwarded-proto': 'https',
            'x-now-deployment-url': 'python-wsgi-test.now.sh',
            'x-now-id': 'insecure-now-id',
            'x-now-log-id': 'insecure-now-log-id',
            'x-now-trace': 'iad1',
            'x-real-ip': '255.255.255.255',
            'x-zeit-co-forwarded-for': '255.255.255.255'
        },
        'host': 'python-wsgi-test.now.sh',
        'method': 'GET',
        'path': '/'
    }),
}


@Request.application
def application(request):
    return Response('Success!')


def test_now_handler_get_request():
    response = handler(application, get_request_event, None)
    assert response['statusCode'] == 200
    assert 'headers' in response
