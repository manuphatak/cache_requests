#!/usr/bin/env python
# coding=utf-8

def test_session_uses_config():
    from cache_requests import config, Session

    config.ex = 10

    requests = Session()
    assert requests.get.ex == 10


def test_memoize_uses_config():
    from cache_requests import config, memoize
    config.ex = 10

    @memoize
    def hello():
        pass

    assert hello.ex == 10
