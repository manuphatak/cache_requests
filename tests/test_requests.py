#!/usr/bin/env python
# coding=utf-8

from mock import MagicMock
from pytest import fixture


@fixture
def mock_requests(monkeypatch, tmpdir):
    """:type request: _pytest.python.FixtureRequest"""
    from cache_requests import Config

    def mock_response(*args, **kwargs):
        return args, kwargs

    mock = MagicMock(spec=mock_response)
    mock.side_effect = mock_response
    monkeypatch.setattr('requests.sessions.Session.get', mock)
    monkeypatch.setattr('requests.sessions.Session.options', mock)
    monkeypatch.setattr('requests.sessions.Session.head', mock)
    monkeypatch.setattr('requests.sessions.Session.post', mock)
    monkeypatch.setattr('requests.sessions.Session.put', mock)
    monkeypatch.setattr('requests.sessions.Session.patch', mock)
    monkeypatch.setattr('requests.sessions.Session.delete', mock)

    Config.ex = 1
    Config.dbfilename = tmpdir.join('test_redis.db').strpath

    return mock


@fixture
def requests():
    from cache_requests.sessions import Session

    return Session()


def test_requests_get_properly_patched(requests, mock_requests):
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


def test_requests_posts_properly_patched(requests, mock_requests):
    mock_requests.assert_not_called()
    requests.post('http://google.com')
    assert mock_requests.call_count == 1
    mock_requests.assert_called_with('http://google.com', data=None, json=None)
