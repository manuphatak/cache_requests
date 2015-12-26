#!/usr/bin/env python
# coding=utf-8
"""
:mod:`cache_requests._compat`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. moduleauthor:: Manu Phatak <bionikspoon@gmail.com>

Python 2to3 compatibility handling.
"""

import logging
from sys import version_info

from six import PY3

PY26 = version_info[0:2] <= (2, 6)
__all__ = ['NullHandler', 'pickle']

if not PY26:
    from logging import NullHandler
else:  # pragma: no cover
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

if PY3:
    import pickle
else:  # pragma: no cover
    # noinspection PyPep8Naming
    import cPickle as pickle
