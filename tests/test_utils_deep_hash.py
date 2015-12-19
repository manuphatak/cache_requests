#!/usr/bin/env python
# coding=utf-8
from copy import deepcopy

from pytest import fixture

from cache_requests.utils import deep_hash


def is_int(p_object):  # Test helper
    return isinstance(p_object, int)


sample_string_1 = 'this is a test'
sample_string_2 = """
                    this is a doc string.
                    with lines.
"""
sample_tuple = sample_string_1, sample_string_2


@fixture
def sample_object():
    return deepcopy({
        "this": ["is", "a", {
            "test": ("of", "hashing", "mixed objects", 42)
        }],
        '42': "what a strange dictionary",
        "done": "completed"
    })


def test_deep_hash_with_string_sample_1():
    assert deep_hash(sample_string_1) == deep_hash(sample_string_1)
    assert is_int(deep_hash(sample_string_1))


def test_deep_hash_with_string_sample_2():
    assert deep_hash(sample_string_2) == deep_hash(sample_string_2)
    assert is_int(deep_hash(sample_string_2))


def test_deep_hash_with_tuple():
    assert deep_hash(sample_tuple) == deep_hash(sample_tuple)
    assert is_int(deep_hash(sample_tuple))


def test_deep_hash_with_mixed_object(sample_object):
    assert is_int(deep_hash(sample_object))
    assert deep_hash(sample_object) == deep_hash(sample_object)


def test_deep_hash_with_gets_same_results_based_on_value(sample_object):
    sample_object_1 = sample_object
    sample_object_2 = deepcopy(sample_object)
    assert deep_hash(sample_object_1) == deep_hash(sample_object_2)

    sample_object_2['this'][2]['test'] = ("of", "hashing", "mixed objects", 42)
    assert deep_hash(sample_object_1) == deep_hash(sample_object_2)
    assert is_int(deep_hash(sample_object_2))


def test_deep_hash_with_mutated_mixed_object(sample_object):
    sample_object_1 = sample_object
    sample_object_2 = deepcopy(sample_object)
    assert deep_hash(sample_object_1) == deep_hash(sample_object_2)

    sample_object_2['this'][2]['test'] = ("of", "ha5hing", "mixed objects", 42)
    assert deep_hash(sample_object_1) != deep_hash(sample_object_2)

    assert is_int(deep_hash(sample_object_2))


def test_deep_hash_args_and_kwargs(sample_object):
    assert deep_hash(*sample_tuple, **sample_object) == deep_hash(*sample_tuple, **sample_object)


def test_deep_hash_args_similiar_values():
    assert deep_hash(1, 2, 'three', '45') != deep_hash(1, 2, 'three3', '45')


def test_can_compare_args_and_kwargs():
    assert deep_hash(1, 2, 'three', 45) != deep_hash(1, 2, 'three', 45, this="test")


def test_can_compare_args_and_kwargs_2():
    assert deep_hash(1, 2, 'three', 45, this="test") != deep_hash(1, 2, 'three', 45, this="not", a="test")
