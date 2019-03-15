#! /usr/bin/env python
import json

from setuptools import setup


with open('package.json') as f:
    package_data = json.loads(f.read())
    version = package_data['version']


"""A barebones setup for tests
"""
setup(
    name='now-python-asgi',
    version=version,
    packages=[
        'now_python_asgi'
    ],
    install_requires=[
    ]
)
