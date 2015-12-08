#!/usr/bin/env python
# coding=utf-8
from cache_requests.cache_requests import deep_hash
from tests import is_int, PY27


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
