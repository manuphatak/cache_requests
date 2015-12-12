#!/usr/bin/env python
# coding=utf-8
"""
:mod:`cache_requests.utils`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: cache_requests.utils
    :synopsis: Package utilities.
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
from __future__ import absolute_import

from collections import namedtuple
from functools import wraps

from ._compat import singledispatch

__all__ = ['AttributeDict', 'normalize_signature', 'deep_hash']


class AttributeDict(object):
    """Strict dict with attribute access"""

    __attr__ = ()
    """Allowed attributes.  Must be explicitly defined."""

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
@singledispatch
def deep_hash(args):
    """
    Recursively hash nested mixed objects (dicts, lists, sets, tuple, hashable objects).

    :param args: Value to hash.
    :return: Hashed value.
    :rtype: int
    """
    return hash(args)


@deep_hash.register(tuple)
@deep_hash.register(set)
@deep_hash.register(list)
def _(args):
    return hash(tuple(deep_hash(item) for item in args))


@deep_hash.register(dict)  # noqa
def _(args):
    args_copy = {}
    for key, value in args.items():
        args_copy[key] = deep_hash(value)
    return hash(frozenset(sorted(args_copy.items())))
