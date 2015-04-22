#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

import requests
from .memoize import Memoize

# monkeypatch + decorate requests library
requests.get = Memoize(requests.get)
requests.post = Memoize(requests.post)

# noinspection PyUnresolvedReferences
from requests import *