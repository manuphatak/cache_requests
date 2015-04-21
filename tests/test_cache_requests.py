#!/usr/bin/env python
# coding=utf-8

"""
test_cache_requests
-------------------

Tests for ``cache_requests`` module.
"""
import pytest



@pytest.fixture
def cache_requests():
    import cache_requests.memoize as mock_cache_requests
    return mock_cache_requests

def test_cache_requests_properly_mocked(cache_requests):
    from cache_requests.memoize import EXPIRATION

    assert EXPIRATION == 3600

def test_intended_use_case():
    import cache_requests as requests

    response = requests.get('http://google.com')

    assert response.text == False