# Changelog


## [1.0.6] - 2019-03-14 - Fixes for base64 encoded bodies

### Changed
- Fixed base64 handling in the handler. Request bodies were previously being
   passed on to the application without decoding, but with padding stripped
   (preventing decoding by the application).


## [1.0.5] - 2019-03-13 - Fixes for querystrings and empty response bodies

### Changed
- Handler is now installed as a python package instead of being copied into the
   project source.
- Querystring handling has been corrected.
- Empty return body handling has been patched to match Now's requirement of a
   `body` object on the response. An empty body is returned if no body is
   supplied by the application.


## [1.0.4] - 2019-03-13 - Ensure logging configuration

### Added
- Logging is now configured with `logging.basicConfig()` in `handler.py` to
   ensure logging is initialized at the module level.


## [1.0.3] - 2019-03-10

### Changed
- Fixed typo in `index.js` which was appearing in logs


## [1.0.2] - 2019-03-10 - Selectable runtime

### Added
- Configuration option `runtime` can now be used to set the lambda runtime,
   e.g., `python3.6`. *The build environment is not affected, beware of
   issues building in Python 3.5 and running and other versions.*

### Changed
- Improved builder log output (`log.js`)
- Consolidated pip activities to `pip.js`

### Removed
- No longer installs `Werkzeug` every time. Projects will need to include
   `Werkzeug` as a dependency in their project `requirements.txt`. If a
   `requirements.txt` file is not found, the builder will install `Werkzeug`
   assuming the project has no other dependencies.


## [1.0.1] - 2019-03-03 - Fix logging

### Added
- Stubbed testing with a single GET request test and test configuration

### Changed
- Removed `print` calls from `now_python_wsgi.handler.handler()` to prevent
   printing sensitive data to longs (e.g., passwords passed in the body of a
   request).


## 1.0.0 - 2019-03-02 - Getting started!
We're just getting started. This establishes a tidy repository ready for the
world.


[1.0.6]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.5...v1.0.6
[1.0.5]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.0...v1.0.1
