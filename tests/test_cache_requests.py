#!/usr/bin/env python
# coding=utf-8

"""
test_cache_requests
----------------------------------

Tests for `cache_requests` module.
"""
import pytest


@pytest.fixture
def cache_requests():
    from cache_requests import cache_requests

    mock_cache_requests = cache_requests()
    return mock_cache_requests

def test_cache_requests_properly_mocked(cache_requests):

    assert str(cache_requests) == "Success"