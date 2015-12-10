#!/usr/bin/env python
# coding=utf-8
from pytest import fixture, raises

from cache_requests.utils import AttributeDict


class Config(AttributeDict):
    __attr__ = 'test',


@fixture
def config():
    return Config(test='success')


def test_get_attr_raises_error_for_missing_attr():

    config = AttributeDict()
    with raises(AttributeError):
        _ = config.fail  # noqa


def test_set_attr_raises_error():
    config = AttributeDict()
    with raises(AttributeError):
        config.fail = 'pass'


def test_dict_like_access(config):
    assert config['test'] == 'success'
    config['test'] = 'success!'
    assert config['test'] == 'success!' == config.test


def test_repr(config):
    assert repr(config) == 'Config(test=\'success\')'
