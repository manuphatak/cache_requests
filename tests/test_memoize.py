#!/usr/bin/env python
# coding=utf-8

"""
test_cache_requests
-------------------

Tests for ``cache_requests`` module.
"""

from mock import MagicMock
from pytest import fixture, raises


@fixture
def amazing_function():
    from cache_requests import Memoize

    def _side_effect(*args, **kwargs):
        return len(args), len(kwargs)

    _amazing_function = MagicMock(spec=_side_effect, side_effect=_side_effect)
    _amazing_function.__name__ = 'amazing_function'
    return Memoize(_amazing_function, ex=1)


def test_memoized_function_called_only_once_per_arguments(amazing_function):
    """
    Function is only called with unique parameters

    :type amazing_function: mock.MagicMock
    """
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
    """:type amazing_function: mock.MagicMock"""

    from cache_requests.utils import deep_hash

    # SETUP
    args, kwargs = ('amazing_function', 1, 2, 'three', 45), dict(this="is not", a="test")
    key = deep_hash(*args, **kwargs)
    assert amazing_function.redis.dbsize() == 0

    assert amazing_function(1, 2, 'three', 45, this="is not", a="test") == (4, 2)

    # TEST EXPIRATION SET
    assert 990 < amazing_function.redis.pttl(key) <= 1000


def test_raises_with_bad_params():
    from cache_requests import Memoize

    with raises(TypeError):
        Memoize(func=1)


def test_decorator_with_params():
    from cache_requests import Memoize

    @Memoize(ex=1)
    def hello():
        pass

    assert hello.ex == 1
    hello()
    assert hello.redis.dbsize() == 0


def test_redis_getter_setter(tmpdir):
    """:type tmpdir: py.path.local"""

    from cache_requests import Memoize
    from redislite import StrictRedis

    # LOCAL SETUP
    # ------------------------------------------------------------------------
    @Memoize(ex=1)
    def hello():
        pass

    test_connection = hello.redis
    test_db = tmpdir.join('test_redis.db').strpath
    alt_db = tmpdir.join('test_redis_getter_setter.db').strpath
    alt_connection = StrictRedis(dbfilename=alt_db)

    # TEST SETUP
    # ------------------------------------------------------------------------
    assert test_connection.db == test_db
    assert alt_connection.db == alt_db
    assert test_db != alt_db

    # TEST MEMOIZE REDIS SETTER
    # ------------------------------------------------------------------------
    hello.redis = alt_connection

    assert hello.redis.db != test_db
    assert hello.redis.db == alt_db


def test_bust_cache_reevaluates_function(redis_mock):
    """:type redis_mock: mock.MagicMock"""

    from cache_requests import Memoize

    # LOCAL TEST HELPER
    # ------------------------------------------------------------------------
    def call_count():
        try:
            return redis_mock.get.call_count, redis_mock.set.call_count
        finally:
            redis_mock.reset_mock()

    # LOCAL SETUP
    # ------------------------------------------------------------------------
    result = {
        'test': 'sample text'
    }

    @Memoize(connection=redis_mock)
    def hello(*_):
        return result.get('test')

    # TEST LOCAL SETUP
    # ------------------------------------------------------------------------
    assert call_count() == (0, 0)

    # 1 get, 1 set
    assert hello('hello', 'world') == 'sample text'
    assert call_count() == (1, 1)

    assert call_count() == (0, 0)

    # TEST GETTING RESULTS FROM CACHE
    # ------------------------------------------------------------------------
    result['test'] = 'bad cache target'

    # 1 get, 0 sets
    assert hello('hello', 'world') == 'sample text'
    assert call_count() == (1, 0)

    # TEST BUSTING CACHE
    # ------------------------------------------------------------------------

    # 0 gets, 1 set
    assert hello('hello', 'world', bust_cache=True) == 'bad cache target'
    assert call_count() == (0, 1)

    # TEST GETTING RESULTS FROM CACHE AFTER BUST
    # ------------------------------------------------------------------------

    # 1 get, 0 sets
    assert hello('hello', 'world') == 'bad cache target'

    # NO FUNNY BUSINESS
    result['test'] = 'really bad cache target'

    # 1 get, 0 sets
    assert hello('hello', 'world') == 'bad cache target'
    assert call_count() == (2, 0)


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


def test_set_cache_cb_is_used_to_skip_cache(redis_mock):
    """:type redis_mock: mock.MagicMock"""

    from cache_requests import Memoize

    # LOCAL TEST HELPER
    # ------------------------------------------------------------------------
    def call_count():
        try:
            return redis_mock.get.call_count, redis_mock.set.call_count
        finally:
            redis_mock.reset_mock()

    # LOCAL SETUP
    # ------------------------------------------------------------------------
    result = {
        'test': 'sample text'
    }

    @Memoize(connection=redis_mock)
    def hello(*_):
        return result.get('test')

    # TEST SETUP
    # ------------------------------------------------------------------------
    assert call_count() == (0, 0)

    # 1 get, 1 set
    assert hello('hello', 'world') == 'sample text'
    assert call_count() == (1, 1)
    assert call_count() == (0, 0)

    # TEST NO CACHE WHEN FALSE
    # ------------------------------------------------------------------------

    assert hello(set_cache=False) == 'sample text'
    assert call_count() == (1, 0)

    result['test'] = 'not using cache'
    assert hello(set_cache=False) == 'not using cache'
    assert call_count() == (1, 0)

    # TEST NO CACHE WHEN CALLBACK IS FALSE
    # ------------------------------------------------------------------------
    result['test'] = 'still not using cache'
    assert hello(set_cache=lambda _: False) == 'still not using cache'
    assert call_count() == (1, 0)

    # TEST CALLBACK THAT USES FUNC RESULTS
    # ------------------------------------------------------------------------

    # setup
    def sample_callback(results):
        return results != 'setup: using results in callback'

    result['test'] = 'setup: using results in callback'
    assert hello(set_cache=sample_callback) == 'setup: using results in callback'
    assert call_count() == (1, 0)

    result['test'] = 'test: using results in callback'
    assert hello(set_cache=sample_callback) == 'test: using results in callback'
    assert call_count() == (1, 1)

    result['test'] = 'test: should still be using last results'
    assert hello(set_cache=sample_callback) == 'test: using results in callback'
    assert call_count() == (1, 0)
