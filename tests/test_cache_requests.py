#!/usr/bin/env python
# coding=utf-8

"""
test_cache_requests
-------------------

Tests for ``cache_requests`` module.
"""
import sys
import time
from functools import wraps

import pytest
from redislite import StrictRedis

from cache_requests.cache_requests import deep_hash

PYPY = '__pypy__' in sys.builtin_module_names
PY27 = sys.version_info[0:2] == (2, 7) and not PYPY


def is_int(variable):
    return not not isinstance(variable, int)


@pytest.fixture
def amazing_function(tmpdir):
    """
    Memoized Decorated function. With a counter
    """
    from cache_requests import redis_memoize

    db_path = tmpdir.join('test_redis.db').strpath

    def counter(function):
        """Count how many times the actual function was called"""

        @wraps(function)
        def wrapper(*args, **kwargs):
            wrapper.calls += 1
            return function(*args, **kwargs)

        wrapper.calls = 0
        return wrapper

    @redis_memoize(ex=1, connection=StrictRedis(dbfilename=db_path))
    @counter
    def _amazing_function(*args, **kwargs):
        """Sample function, return tuple of length of args and kwargs"""
        return len(args), len(kwargs)

    assert _amazing_function.function.calls == 0

    return _amazing_function


def test_make_hash_string():
    """Freeze results"""
    assert deep_hash('this is a test') == deep_hash('this is a test')
    assert is_int(deep_hash('this is a test'))
    assert is_int(deep_hash('this is a test '))

    if PY27:
        assert deep_hash('this is a test') == -7693282272941567447
        assert deep_hash('this is a test ') == 1496872550775508506


def test_make_hash_tuple_of_strings():
    """Freeze results"""
    test_tuple = ('this is a test', 'And another')
    assert deep_hash(test_tuple) == deep_hash(test_tuple)

    hash_1, hash_2 = deep_hash(test_tuple)

    assert is_int(hash_1)
    assert is_int(hash_2)

    if PY27:
        assert deep_hash(test_tuple) == (-7693282272941567447, 503894645807253565)


def test_make_hash_mixed():
    """Freeze results"""

    mixed_object = {
        "this": ["is", "a", {
            "test": ("of", "hashing", "mixed objects", 42)
        }],
        '42': "what a strange dictionary",
        "done": "completed"
    }
    assert is_int(deep_hash(mixed_object))
    if PY27:
        assert deep_hash(mixed_object) == -2248685659113089918
    assert deep_hash(mixed_object) == deep_hash(mixed_object)

    mixed_object['this'][2]['test'] = ("of", "hashing", "mixed objects", 42)
    assert is_int(deep_hash(mixed_object))
    if PY27:
        assert deep_hash(mixed_object) == -2248685659113089918

    mixed_object['this'][2]['test'] = ("of", "ha5hing", "mixed objects", 42)
    assert is_int(deep_hash(mixed_object))
    if PY27:
        assert deep_hash(mixed_object) == 5850416323757308216


def test_memoized_decorated_function_only_calls_function_once(amazing_function):
    """Function is only called with unique parameters"""
    assert amazing_function.redis.dbsize() == 0
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
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test", or_is="it?") == (4, 3)
    assert amazing_function.function.calls == 8
    assert amazing_function.redis.dbsize() == 8
    assert amazing_function.redis.flushdb()
    assert amazing_function.redis.dbsize() == 0


def test_memoized_expiration(amazing_function):
    assert amazing_function.redis.dbsize() == 0
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
