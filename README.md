# now-python-wsgi
*A Now builder for Python WSGI applications*

## Quickstart

If you have an existing WSGI app, getting this builder to work for you is a
piece of 🍰!


### 1. Add a Now configuration

Add a `now.json` file to the root of your application:

```json
{
    "version": 2,
    "name": "python-wsgi-app",
    "builds": [{
        "src": "index.py",
        "use": "@ardent-labs/now-python-wsgi",
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
# For a Dango app
from django_app.wsgi import application
# Replace `django_app` with the appropriate name to point towards your project's
# wsgi.py file
```

Look at your framework documentation for help getting access to the WSGI
application.

If the WSGI instance isn't named `application` you'll need adjust the import so
the builder can find it when your project is being deployed. E.g.:

```python
from my_app.wsgi import app as application
```


### 3. Deploy!

That's it, you're ready to go:

```
$ now
> Deploying python-wsgi-app
...
> Success! Deployment ready [57s]
```


## Additional considerations

### Requirements & runtime

At the time of writing, Zeit Now runs on AWS Lambda in the python 3.6 runtime.
This has a number of implications on what libaries will be available to you,
notably:

- PostgreSQL, so psycopg2 won't work out of the box
- MySQL, so MySQL adapters won't work out of the box either
- Sqlite, so the built-in Sqlite adapter won't be available
- Python <3.6, so python 2 code will need an update


## Contributing

### To-dos

- [ ] Add tests for various types of requests


## Attribution

This implementation draws upon work from:

- [@clement](https://github.com/rclement) on
   [now-builders/#163](https://github.com/zeit/now-builders/pull/163)
- [serverless](https://github.com/serverless/serverless) and
   [serverless-wsgi](https://github.com/logandk/serverless-wsgi)
- [@sisp](https://github.com/sisp) on
   [now-builders/#95](https://github.com/zeit/now-builders/pull/95)
- [Zappa](https://github.com/Miserlou/Zappa) by
   [@miserlou](https://github.com/Miserlou)
