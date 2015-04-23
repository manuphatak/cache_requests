#!/usr/bin/env python
# coding=utf-8

"""
test_cache_requests
-------------------

Tests for ``cache_requests`` module.
"""
from functools import wraps
import time

import pytest
import redislite
import sys

PYPY = '__pypy__' in sys.builtin_module_names
PY27 = sys.version_info[0:2] == (2, 7) and not PYPY
is_int = lambda x: isinstance(x, int)


@pytest.fixture
def memoize():
    from cache_requests import memoize

    return memoize


@pytest.fixture
def amazing_function(tmpdir):
    """
    Memoized Decorated function. With a counter
    """
    from cache_requests.memoize import Memoize

    db_path = tmpdir.join('test_redis.db').strpath

    Memoize._redis_connection = redislite.StrictRedis(dbfilename=db_path)
    Memoize._redis_expiration = 1

    def counter(function):
        """Count how many times the actual function was called"""

        @wraps(function)
        def wrapper(*args, **kwargs):
            wrapper.calls += 1
            return function(*args, **kwargs)

        wrapper.calls = 0
        return wrapper

    @Memoize
    @counter
    def amazing_function_(*args, **kwargs):
        """Sample function, return tuple of length of args and kwargs"""
        return len(args), len(kwargs)

    assert amazing_function_.function.calls == 0

    return amazing_function_


def test_make_hash_string(memoize):
    """Freeze results"""
    assert memoize.make_hash('this is a test') == memoize.make_hash('this is a test')
    assert is_int(memoize.make_hash('this is a test'))
    assert is_int(memoize.make_hash('this is a test '))

    if PY27:
        assert memoize.make_hash('this is a test') == -7693282272941567447
        assert memoize.make_hash('this is a test ') == 1496872550775508506


def test_make_hash_tuple_of_strings(memoize):
    """Freeze results"""
    test_tuple = ('this is a test', 'And another')
    assert memoize.make_hash(test_tuple) == memoize.make_hash(test_tuple)

    hash_1, hash_2 = memoize.make_hash(test_tuple)

    assert is_int(hash_1)
    assert is_int(hash_2)

    if PY27:
        assert memoize.make_hash(test_tuple) == (-7693282272941567447, 503894645807253565)


def test_make_hash_mixed(memoize):
    """Freeze results"""

    mixed_object = {"this": ["is", "a", {"test": ("of", "hashing", "mixed objects", 42)}],
                    '42': "what a strange dictionary", "done": "completed"}
    assert is_int(memoize.make_hash(mixed_object))
    if PY27:
        assert memoize.make_hash(mixed_object) == -2248685659113089918
    assert memoize.make_hash(mixed_object) == memoize.make_hash(mixed_object)

    mixed_object['this'][2]['test'] = ("of", "hashing", "mixed objects", 42)
    assert is_int(memoize.make_hash(mixed_object))
    if PY27:
        assert memoize.make_hash(mixed_object) == -2248685659113089918

    mixed_object['this'][2]['test'] = ("of", "ha5hing", "mixed objects", 42)
    assert is_int(memoize.make_hash(mixed_object))
    if PY27:
        assert memoize.make_hash(mixed_object) == 5850416323757308216


def test_memoized_decorated_function_only_calls_function_once(amazing_function):
    """Function is only called with unique parameters"""

    assert amazing_function.function.calls == 0
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function.function.calls == 1
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function.function.calls == 1
    assert amazing_function(1, 2, 'three3', '45') == (4, 0)
    assert amazing_function.function.calls == 2
    assert amazing_function(1, 3, 'three', '45') == (4, 0)
    assert amazing_function.function.calls == 3
    assert amazing_function(1, 2, 'three', 45) == (4, 0)
    assert amazing_function.function.calls == 4

    assert amazing_function(1, 2, 'three', 45, this="test") == (4, 1)
    assert amazing_function.function.calls == 5

    assert amazing_function(1, 2, 'three', 45, this="not", a="test") == (4, 2)
    assert amazing_function.function.calls == 6

    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.calls == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.calls == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.calls == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.calls == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test", or_is="it?") == (
        4, 3)
    assert amazing_function.function.calls == 8


def test_memoized_expiration(amazing_function, ):
    assert amazing_function.function.calls == 0
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.calls == 1
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.calls == 1
    time.sleep(1)
    assert amazing_function.function.calls == 1
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)

    assert amazing_function.function.calls == 2


