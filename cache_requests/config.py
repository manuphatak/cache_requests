#!/usr/bin/env python
# coding=utf-8
import os

EXPIRATION = os.environ.get('EXPIRATION', 60 * 60)
REDISLITE_DB = os.environ.get('REDISLITE_DB', 'cache_requests.redislite')
REDIS_CONNECTION = os.environ.get('REDIS_CONNECTION', None)