#!/usr/bin/env python
# coding=utf-8
from importlib import reload

from mock import MagicMock
from pytest import fixture


@fixture
def mock_requests(monkeypatch, tmpdir):
    """:type request: _pytest.python.FixtureRequest"""
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
    import requests

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
    import requests

    mock_requests.assert_not_called()
    requests.post('http://google.com')
    assert mock_requests.call_count == 1
    mock_requests.assert_called_with('http://google.com')


# def test_unpatch_request():
#     import requests
#     from cache_requests import patch_requests
#
#     archive = {}
#     archive['get'] = requests.get
#     archive['post'] = requests.post
#     assert archive['get'] is requests.get
#     assert archive['post'] is requests.post
#     patch_requests()
#     reload(requests)
#     assert hasattr(requests.get, 'redis')
#     # assert archive['get'] != requests.get
#     # assert archive['post'] is not requests.post
