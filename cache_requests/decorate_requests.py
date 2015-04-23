#!/usr/bin/env python
# coding=utf-8
"""
decorate_requests module
------------------------

This module monkey patches the requests library with a decorators.
"""
from __future__ import absolute_import

import requests
from .memoize import Memoize

# monkeypatch + decorate requests library
requests.get = Memoize(requests.get)
requests.post = Memoize(requests.post)

# noinspection PyUnresolvedReferences
from requests import *