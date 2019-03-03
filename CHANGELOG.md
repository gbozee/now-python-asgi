# Changelog

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


[1.0.1]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.0...v1.0.1
