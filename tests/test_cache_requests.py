#!/usr/bin/env python
# coding=utf-8

"""
test_cache_requests
-------------------

Tests for ``cache_requests`` module.
"""
import time
from functools import wraps

from pytest import fixture


@fixture
def amazing_function(tmpdir, request):
    """
    Memoized Decorated function. With a counter
    :param _pytest.python.FixtureRequest request:

    """
    from cache_requests import redis_memoize
    from redislite import StrictRedis

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
