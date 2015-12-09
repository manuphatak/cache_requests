#!/usr/bin/env python
# coding=utf-8

import requests
from mock import MagicMock
from pytest import fixture


@fixture(autouse=True)
def mock_requests(monkeypatch, tmpdir):
    from cache_requests import patch_requests, Config

    def get(*args, **kwargs):
        return args, kwargs

    mock = MagicMock(spec=get)
    mock.side_effect = get
    monkeypatch.setattr('requests.get', mock)
    monkeypatch.setattr('requests.post', mock)
    monkeypatch.delattr("requests.sessions.Session.request")

    Config.ex = 1
    Config.dbfilename = tmpdir.join('test_redis.db').strpath
    patch_requests()

    return mock


def test_requests_get_properly_patched(mock_requests):
    mock_requests.assert_not_called()
    # 1st unique call
    requests.get('http://google.com')
    assert mock_requests.call_count == 1
    requests.get('http://google.com')
    requests.get('http://google.com')
    assert mock_requests.call_count == 1

    headers = {
        "accept-encoding": "gzip, deflate, sdch",
        "accept-language": "en-US,en;q=0.8"
    }
    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
                   q="hash%20a%20dictionary%20python")
    # 2nd unique call
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert mock_requests.call_count == 2
    requests.get('http://google.com/search', headers=headers, params=payload)
    requests.get('http://google.com/search', headers=headers, params=payload)
    requests.get('http://google.com/search', headers=headers, params=payload)
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert mock_requests.call_count == 2

    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
                   q="hash%20a%20dictionary%20python2")
    # 3rd unique call
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert mock_requests.call_count == 3
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert mock_requests.call_count == 3


def test_requests_posts_properly_patched(mock_requests):
    mock_requests.assert_not_called()
    requests.post('http://google.com')
    assert mock_requests.call_count == 1
    mock_requests.assert_called_with('http://google.com')
