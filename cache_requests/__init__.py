#!/usr/bin/env python
# coding=utf-8
"""
Persistent lru caching of the requests library.
"""

__author__ = 'Manu Phatak'
__email__ = 'bionikspoon@gmail.com'
__version__ = '0.1.0'

from requests import *
import cache_requests

# monkeypatch + decorate requests library
get = cache_requests.Memoize(get)
post = cache_requests.Memoize(post)
