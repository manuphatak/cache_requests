#!/usr/bin/env python
# coding=utf-8
"""
:mod:`cache_requests.config`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. moduleauthor:: Manu Phatak <bionikspoon@gmail.com>

Global config, default package settings.

.. note:: Environment variables are all caps prefixed with ``REDIS_``

.. data:: ex

    Default expiration for cached keys in seconds.

    :default: ``3600``  # 1 hour

    :env: :envvar:`REDIS_EX`

    .. tip:: Set to ``None`` for permanent caching.

.. data:: dbfilename

    Filepath for :mod:`redislite` connection.

    :default: ``temp_file('cache_requests.redislite')``

    :env: :envvar:`REDIS_EX`

    .. tip:: :mod:`redislite` will automatically use a unique tmp file if this is set to ``None``.  This can be used to turn off persistence between sessions.

    .. note:: :mod:`redislite` will NOT implicitly create directories.

.. data:: connection

    Callback to create a :mod:`redislite` connection handle.  This can be either callable or already opened.

    :default: ``functools.partial(redislite.StrictRedis, dbfilename=config.dbfilename)``

    :env: :envvar:`REDIS_CONNECTION`

    .. tip:: Use a :mod:`redis` connection here as a drop in replacement.


"""
from __future__ import absolute_import

from functools import partial
from os import environ, path
from tempfile import gettempdir

from redislite import StrictRedis

temp_file = partial(path.join, gettempdir())

__all__ = ['ex', 'dbfilename', 'connection']

ex = environ.get('REDIS_EX', 60 * 60)  # 1 hour
dbfilename = environ.get('REDIS_DBFILENAME', temp_file('cache_requests.redislite'))
connection = environ.get('REDIS_CONNECTION') or partial(StrictRedis, dbfilename=dbfilename)
