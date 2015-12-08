#!/usr/bin/env python
# coding=utf-8

"""
test_cache_requests
-------------------

Tests for ``cache_requests`` module.
"""
import time

from mock import Mock
from pytest import fixture


@fixture
def amazing_function(tmpdir):
    """
    :param py.path.local tmpdir:
    """
    from cache_requests import redis_memoize
    from redislite import StrictRedis

    db_path = tmpdir.join('test_redis.db').strpath
    connection = StrictRedis(dbfilename=db_path)
    wrapper = redis_memoize(ex=1, connection=connection)
    _amazing_function = Mock()
    _amazing_function.side_effect = lambda *args, **kwargs: (len(args), len(kwargs))
    _amazing_function = wrapper(_amazing_function)

    return _amazing_function


def test_memoized_functions_called_only_once(amazing_function):
    """Function is only called with unique parameters"""
    assert amazing_function.redis.dbsize() == 0
    assert amazing_function.function.call_count == 0
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function.function.call_count == 1
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function.function.call_count == 1
    assert amazing_function(1, 2, 'three3', '45') == (4, 0)
    assert amazing_function.function.call_count == 2
    assert amazing_function(1, 3, 'three', '45') == (4, 0)
    assert amazing_function.function.call_count == 3
    assert amazing_function(1, 2, 'three', 45) == (4, 0)
    assert amazing_function.function.call_count == 4

    assert amazing_function(1, 2, 'three', 45, this="test") == (4, 1)
    assert amazing_function.function.call_count == 5

    assert amazing_function(1, 2, 'three', 45, this="not", a="test") == (4, 2)
    assert amazing_function.function.call_count == 6

    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.call_count == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.call_count == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.call_count == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.call_count == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test", or_is="it?") == (4, 3)
    assert amazing_function.function.call_count == 8
    assert amazing_function.redis.dbsize() == 8
    assert amazing_function.redis.flushdb()
    assert amazing_function.redis.dbsize() == 0


def test_memoized_expiration(amazing_function):
    assert amazing_function.redis.dbsize() == 0
    assert amazing_function.function.call_count == 0
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.call_count == 1
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.function.call_count == 1
    time.sleep(1)
    assert amazing_function.function.call_count == 1
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)

    assert amazing_function.function.call_count == 2
