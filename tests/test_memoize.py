#!/usr/bin/env python
# coding=utf-8

"""
test_cache_requests
-------------------

Tests for ``cache_requests`` module.
"""
import time

from mock import MagicMock
from pytest import fixture, raises


@fixture
def amazing_function():
    from cache_requests import config
    from redislite import StrictRedis
    from cache_requests import Memoize

    def _side_effect(*args, **kwargs):
        return len(args), len(kwargs)

    _amazing_function = MagicMock(spec=_side_effect, side_effect=_side_effect)

    connection = StrictRedis(dbfilename=config.dbfilename)

    return Memoize(_amazing_function, ex=1, connection=connection)


def test_memoized_function_called_only_once_per_arguments(amazing_function):
    """Function is only called with unique parameters"""

    assert amazing_function.redis.dbsize() == 0
    assert amazing_function.func.call_count == 0
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function.func.call_count == 1
    assert amazing_function(1, 2, 'three', '45') == (4, 0)
    assert amazing_function.func.call_count == 1
    assert amazing_function(1, 2, 'three3', '45') == (4, 0)
    assert amazing_function.func.call_count == 2
    assert amazing_function(1, 3, 'three', '45') == (4, 0)
    assert amazing_function.func.call_count == 3
    assert amazing_function(1, 2, 'three', 45) == (4, 0)
    assert amazing_function.func.call_count == 4

    assert amazing_function(1, 2, 'three', 45, this="test") == (4, 1)
    assert amazing_function.func.call_count == 5

    assert amazing_function(1, 2, 'three', 45, this="not", a="test") == (4, 2)
    assert amazing_function.func.call_count == 6

    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.func.call_count == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.func.call_count == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.func.call_count == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.func.call_count == 7
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test", or_is="it?") == (4, 3)
    assert amazing_function.func.call_count == 8
    assert amazing_function.redis.dbsize() == 8
    assert amazing_function.redis.flushdb()
    assert amazing_function.redis.dbsize() == 0


def test_expiration(amazing_function):
    assert amazing_function.redis.dbsize() == 0
    assert amazing_function.func.call_count == 0
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.func.call_count == 1
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)
    assert amazing_function.func.call_count == 1
    time.sleep(1)
    assert amazing_function.func.call_count == 1
    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)

    assert amazing_function.func.call_count == 2


def test_raises_with_bad_params():
    from cache_requests import Memoize

    with raises(TypeError):
        Memoize(func=1)


def test_access_to_memoized_functions_attributes():
    from cache_requests import Memoize, config

    config.ex = 1

    @Memoize
    def hello():
        pass

    assert hello.ex == 1 == config.ex


def test_decorator_with_params():
    from cache_requests import Memoize, config

    assert config.ex == 3600

    @Memoize(ex=1)
    def hello():
        pass

    assert hello.ex == 1
    hello()
    assert hello.redis.dbsize() == 0


def test_kwarg_to_optionally_cache(MockRedis):
    """:type MockRedis: mock.MagicMock"""

    from cache_requests import Memoize

    MockRedis.assert_not_called()
    MockRedis.get.assert_not_called()
    MockRedis.set.assert_not_called()

    result = {
        'test': 'sample text'
    }

    @Memoize
    def hello(*_):
        return result.get('test')

    MockRedis.get.assert_not_called()
    MockRedis.set.assert_not_called()

    assert hello('hello', 'world') == 'sample text'

    assert MockRedis.set.call_count == 1
    assert MockRedis.get.call_count == 1

    result['test'] = 'bad cache target'
    assert hello('hello', 'world') == 'sample text'

    assert MockRedis.set.call_count == 1
    assert MockRedis.get.call_count == 2

    assert hello('hello', 'world', bust_cache=True) == 'bad cache target'

    assert MockRedis.set.call_count == 2
    assert MockRedis.get.call_count == 3

    assert hello('hello', 'world') == 'bad cache target'

    assert MockRedis.set.call_count == 2
    assert MockRedis.get.call_count == 4

    result['test'] = 'really bad cache target'
    assert hello('hello', 'world') == 'bad cache target'

    assert MockRedis.set.call_count == 2
    assert MockRedis.get.call_count == 5


def test_cache_results_are_unique_per_function():
    from cache_requests import Memoize

    @Memoize
    def hello(*args, **kwargs):
        return len(args), len(kwargs)

    @Memoize
    def world(*args, **kwargs):
        return len(args) * len(kwargs)

    test_args = 'I', 'Like', 'Turtles'

    assert hello(*test_args) != world(*test_args)

def test_callback_to_optionally_cache(MockRedis):
    """:type MockRedis: mock.MagicMock"""

    from cache_requests import Memoize

    MockRedis.assert_not_called()
    MockRedis.get.assert_not_called()
    MockRedis.set.assert_not_called()

    result = {
        'test': 'sample text'
    }

    @Memoize
    def hello(*_):
        return result.get('test')

    MockRedis.get.assert_not_called()
    MockRedis.set.assert_not_called()

    assert hello(set_cache=False) == 'sample text'

    result['test'] = 'not using cache'
    assert hello(set_cache=False) == 'not using cache'

    result['test'] = 'still not using cache'
    assert hello(set_cache=lambda _:False) == 'still not using cache'

    def sample_callback(results):
        return results != 'setup: using results in callback'

    result['test'] = 'setup: using results in callback'
    assert hello(set_cache=sample_callback) == 'setup: using results in callback'

    result['test'] = 'test: using results in callback'
    assert hello(set_cache=sample_callback) == 'test: using results in callback'

    result['test'] = 'test: should still be using last results'
    assert hello(set_cache=sample_callback) == 'test: using results in callback'
