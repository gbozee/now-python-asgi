# now-python-asgi
*A Now builder for Python ASGI applications*

<!-- [![NPM version](https://img.shields.io/npm/v/@ardent-labs/now-python-wsgi.svg)](https://www.npmjs.com/package/@ardent-labs/now-python-wsgi)
[![Build Status](https://travis-ci.org/ardent-co/now-python-wsgi.svg?branch=master)](https://travis-ci.org/ardent-co/now-python-wsgi)
[![License](https://img.shields.io/npm/l/@ardent-labs/now-python-wsgi.svg)](https://github.com/ardent-co/now-python-wsgi/blob/master/LICENSE) -->

## Quickstart

If you have an existing WSGI app, getting this builder to work for you is a
piece of 🍰!


### 1. Add a Now configuration

Add a `now.json` file to the root of your application:

```json
{
    "version": 2,
    "name": "python-asgi-app",
    "builds": [{
        "src": "index.py",
        "use": "@gbozee/now-python-asgi",
        "config": { "maxLambdaSize": "15mb" }
    }]
}
```

This configuration is doing a few things in the `"builds"` part:

1. `"src": "index.py"`
   This tells Now that there is one entrypoint to build for. `index.py` is a
   file we'll create shortly.
2. `"use": "@ardent-labs/now-python-wsgi"`
   Tell Now to use this builder when deploying your application
3. `"config": { "maxLambdaSize": "15mb" }`
   Bump up the maximum size of the built application to accommodate some larger
   python WSGI libraries (like Django or Flask). This may not be necessary for
   you.


### 2. Add a Now entrypoint

Add `index.py` to the root of your application. This entrypoint should make
available an object named `application` that is an instance of your WSGI
application. E.g.:

```python
# For a sample Starlette app
from starlette.applications import Starlette
from starlette.responses import JSONResponse

application = Starlette()

@application.route('/')
async def homepage(request):
    return JSONResponse({'hello': 'world'})

# Replace `django_app` with the appropriate name to point towards your project's
# wsgi.py file
```

If the ASGI instance isn't named `application` you can set the
`wsgiApplicationName` configuration option to match your application's name (see
the configuration section below).


### 3. Deploy!

That's it, you're ready to go:

```
$ now
> Deploying python-asgi-app
...
> Success! Deployment ready [57s]
```


## Requirements

Your project may optionally include a `requirements.txt` file to declare any
dependencies. 


## Configuration options

### `runtime`

Select the lambda runtime. Defaults to `python3.7`.
```json
{
    "builds": [{
        "config": { "runtime": "python3.7" }
    }]
}
```


### `wsgiApplicationName`

Select the WSGI application to run from your entrypoint. Defaults to
`application`.
```json
{
    "builds": [{
        "config": { "asgiApplicationName": "application" }
    }]
}
```


## Additional considerations

### Routing

You'll likely want all requests arriving at your deployment url to be routed to
your application. You can do this by adding a route rewrite to the Now
configuration:
```json
{
    "version": 2,
    "name": "python-asgi-app",
    "builds": [{
        "src": "index.py",
        "use": "@gbozee/now-python-asgi"
    }],
    "routes" : [{
        "src" : "/(.*)", "dest":"/"
    }]
}
```

### Avoiding the `index.py` file

If having an extra file in your project is troublesome or seems unecessary, it's
also possible to configure Now to use your application directly, without passing
it through `index.py`.

If your WSGI application lives in `now_app/wsgi.py` and is named `application`,
then you can configure it as the entrypoint and adjust routes accordingly:
```json
{
    "version": 2,
    "name": "python-asgi-app",
    "builds": [{
        "src": "now_app/asgi.py",
        "use": "@gbozee/now-python-asgi"
    }],
    "routes" : [{
        "src" : "/(.*)", "dest":"/now_app/asgi.py"
    }]
}
```

### Lambda environment limitations

At the time of writing, Zeit Now runs on AWS Lambda. This has a number of
implications on what libaries will be available to you, notably:

- PostgreSQL, so psycopg2 won't work out of the box
- MySQL, so MySQL adapters won't work out of the box either
- Sqlite, so the built-in Sqlite adapter won't be available


## Contributing

### To-dos

- [ ] Add tests for various types of requests


## Attribution

This implementation draws upon work from:

- [@erm](https://github.com/erm) on [mangum](https://github.com/erm/mangum)
- [@ardent-co](https://github.com/ardent-co) on 
  [now-python-wsgi](https://github.com/ardent-co/now-python-wsgi)
