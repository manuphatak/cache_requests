#!/usr/bin/env python
# coding=utf-8
"""
:mod:`cache_requests.utils`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. moduleauthor:: Manu Phatak <bionikspoon@gmail.com>

Package utilities.

Private API
***********
    * :class:`AttributeDict`
    * :func:`deep_hash`
    * :func:`normalize_signature`

Source
******

"""
from __future__ import absolute_import, unicode_literals

import sys
from collections import namedtuple
from functools import partial, wraps
from hashlib import md5
from tempfile import gettempdir

from os import path
from redislite import StrictRedis
from six import string_types, text_type, integer_types

__all__ = ['AttributeDict', 'deep_hash', 'default_connection', 'default_ex', 'normalize_signature', 'make_callback',
           'temp_file']


def temp_file(name):
    return temp_file_partial('%s.cache_requests.redislite.db' % name)


def guess_caller():
    file_name = path.splitext(path.split(sys.argv[0])[-1])[0]

    if len(sys.argv) > 1:
        # noinspection PyBroadException
        try:
            suffix = path.splitext(path.split(sys.argv[-1])[-1])[0]
            file_name = '%s_%s' % (file_name, suffix)
        except:  # catch all, do not be the point of failure to end user.
            pass
    return file_name


temp_file_partial = partial(path.join, gettempdir())
default_ex = 3600
default_connection = partial(StrictRedis, dbfilename=temp_file(guess_caller()))


def make_callback(value):
    """Convert bool values to callback"""
    return value if callable(value) else lambda *args, **kwargs: value


class AttributeDict(object):
    """Strict dict with attribute access"""

    __attr__ = ()
    """Attribute white list.  Must be explicitly set."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            msg = 'Attribute %s does not exist.  Attributes: %s', (name, ', '.join(self.__attr__))
            raise AttributeError(msg)

    def __setattr__(self, key, value):
        if key not in self.__attr__:
            msg = 'Can not set attribute %s. Attributes: %s' % (key, ', '.join(self.__attr__))
            raise AttributeError(msg)

        self.__dict__[key] = value

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self):
        _info = namedtuple(self.__class__.__name__, self.__attr__)
        return repr(_info(**self.__dict__))


def normalize_signature(func):
    """Decorator.  Combine args and kwargs. Unpack single item tuples."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs:
            args = args, kwargs

        if len(args) is 1:
            args = args[0]

        return func(args)

    return wrapper


@normalize_signature
def deep_hash(obj):
    hasher = DataHasher()
    hasher.update(obj)
    return hasher.digest()


class DataHasher(object):
    def __init__(self):
        self.md5 = md5()

    def update(self, obj):

        self.md5.update(text_type(type(obj)).encode())

        if isinstance(obj, string_types):
            self.md5.update(obj.encode())
            return self

        if isinstance(obj, (integer_types, float)):
            self.update(text_type(obj))
            return self

        if isinstance(obj, (tuple, list, set)):
            for item in obj:
                self.update(item)
            return self

        if isinstance(obj, dict):
            for key, value in sorted(obj.items()):
                self.update(key)
                self.update(value)
            return self

        for attr in dir(obj):

            # Guard, un serializable attributes
            if attr.startswith('__'):
                continue

            # Guard, mock objects / added by inspection tools
            if attr.startswith('func_'):
                continue

            attr_value = getattr(obj, attr)

            # Guard, functions
            if callable(attr_value):
                continue

            self.update(attr)
            self.update(attr_value)
        return self

    def digest(self):
        return self.md5.hexdigest()
