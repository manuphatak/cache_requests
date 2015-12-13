#!/usr/bin/env python
# coding=utf-8
"""
:mod:`cache_requests._compat`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. moduleauthor:: Manu Phatak <bionikspoon@gmail.com>

Python 2to3 compatibility handling.
"""
import logging

__all__ = ['NullHandler', 'pickle', 'singledispatch']

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:  # pragma: no cover
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

try:
    # noinspection PyPep8Naming
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from functools import singledispatch
except ImportError:  # pragma: no cover
    from singledispatch import singledispatch
