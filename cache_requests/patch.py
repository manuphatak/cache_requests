#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from collections import defaultdict
from importlib import reload

import requests

original_modules = defaultdict(lambda: None)
requests_patched = False

__all__ = ['patch_requests', 'unpatch_requests']


def _patch_requests():
    from . import redis_memoize, Config

    # monkeypatch + decorate requests library
    requests.get = redis_memoize(requests.get, ex=Config.ex, connection=Config.connection)
    requests.post = redis_memoize(requests.post, ex=Config.ex, connection=Config.connection)
    return requests


def patch_requests():
    global original_modules
    global requests_patched
    global requests

    if requests_patched:
        return

    # noinspection PyUnresolvedReferences
    original_modules['requests'] = requests
    _patch_requests()
    requests_patched = True


def unpatch_requests():
    global original_modules
    global requests_patched
    global requests

    if original_modules.get('requests'):
        requests = original_modules['requests']
        original_modules['requests'] = None
    requests_patched = False
