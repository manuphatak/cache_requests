#!/usr/bin/env python
# coding=utf-8
import os

EXPIRATION = 60 * 60  # 1 hour
REDISLITE_DB = os.environ.get('REDISLITE_DB')
REDIS_CONNECTION = None