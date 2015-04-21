#!/usr/bin/env python
# coding=utf-8

# monkeypatch + decorate requests library
import requests
import memoize



requests.get = memoize.Memoize(requests.get)
requests.post = memoize.Memoize(requests.post)
from requests import *