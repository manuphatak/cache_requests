#!/usr/bin/env python
# coding=utf-8

from mock import MagicMock
from pytest import fixture, mark


@fixture
def requests_session_mock():
    def mock_response(*args, **kwargs):
        return args, kwargs

    mock = MagicMock()
    mock.side_effect = mock_response
    mock.status_code = 200

    return mock


@fixture
def patch_requests(monkeypatch, requests_session_mock):
    monkeypatch.setattr('requests.sessions.Session.request', requests_session_mock)


@fixture
def requests():
    from cache_requests.sessions import Session

    return Session()


@mark.usefixtures('patch_requests')
def test_requests_get(requests, requests_session_mock):
    requests_session_mock.assert_not_called()
    # 1st unique call
    requests.get('http://google.com')
    assert requests_session_mock.call_count == 1
    requests.get('http://google.com')
    requests.get('http://google.com')
    assert requests_session_mock.call_count == 1

    headers = {
        "accept-encoding": "gzip, deflate, sdch",
        "accept-language": "en-US,en;q=0.8"
    }
    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
                   q="hash%20a%20dictionary%20python")
    # 2nd unique call
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert requests_session_mock.call_count == 2
    requests.get('http://google.com/search', headers=headers, params=payload)
    requests.get('http://google.com/search', headers=headers, params=payload)
    requests.get('http://google.com/search', headers=headers, params=payload)
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert requests_session_mock.call_count == 2

    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
                   q="hash%20a%20dictionary%20python2")
    # 3rd unique call
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert requests_session_mock.call_count == 3
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert requests_session_mock.call_count == 3


@mark.usefixtures('patch_requests')
def test_requests_options(requests, requests_session_mock):
    requests_session_mock.assert_not_called()
    requests.options('http://google.com')
    requests.options('http://google.com')
    assert requests_session_mock.call_count == 1
    requests_session_mock.assert_called_with('OPTIONS', 'http://google.com', allow_redirects=True)


@mark.usefixtures('patch_requests')
def test_requests_head(requests, requests_session_mock):
    requests_session_mock.assert_not_called()
    requests.head('http://google.com')
    requests.head('http://google.com')
    assert requests_session_mock.call_count == 1
    requests_session_mock.assert_called_with('HEAD', 'http://google.com', allow_redirects=False)


@mark.usefixtures('patch_requests')
def test_requests_post(requests, requests_session_mock):
    requests.cache.post = True

    requests_session_mock.assert_not_called()
    requests.post('http://google.com')
    requests.post('http://google.com')
    assert requests_session_mock.call_count == 1
    requests_session_mock.assert_called_with('POST', 'http://google.com', data=None, json=None)


@mark.usefixtures('patch_requests')
def test_requests_put(requests, requests_session_mock):
    requests.cache.put = True

    requests_session_mock.assert_not_called()
    requests.put('http://google.com')
    requests.put('http://google.com')
    assert requests_session_mock.call_count == 1
    requests_session_mock.assert_called_with('PUT', 'http://google.com', data=None)


@mark.usefixtures('patch_requests')
def test_requests_patch(requests, requests_session_mock):
    requests.cache.patch = True

    requests_session_mock.assert_not_called()
    requests.patch('http://google.com')
    requests.patch('http://google.com')
    assert requests_session_mock.call_count == 1
    requests_session_mock.assert_called_with('PATCH', 'http://google.com', data=None)


@mark.usefixtures('patch_requests')
def test_requests_delete(requests, requests_session_mock):
    requests.cache.delete = True

    requests_session_mock.assert_not_called()
    requests.delete('http://google.com')
    requests.delete('http://google.com')
    assert requests_session_mock.call_count == 1
    requests_session_mock.assert_called_with('DELETE', 'http://google.com')


@mark.usefixtures('patch_requests')
def test_memoize_toggled_off(requests, requests_session_mock):
    requests.cache.get = False

    requests_session_mock.assert_not_called()
    requests.get('http://google.com')
    requests.get('http://google.com')
    assert requests_session_mock.call_count == 2


@mark.usefixtures('patch_requests')
def test_only_cache_200_response(requests, redis_mock):
    requests.get.connection = redis_mock

    redis_mock.assert_not_called()
    redis_mock.get.assert_not_called()
    redis_mock.set.assert_not_called()

    requests.get('http://google.com')
    requests.get('http://google.com')

    assert redis_mock.get.call_count == 2
    assert redis_mock.set.call_count == 1
