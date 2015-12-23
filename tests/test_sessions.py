#!/usr/bin/env python
# coding=utf-8
from mock import MagicMock, Mock
from pytest import fixture, mark


@fixture
def mock_session_request():
    from requests import Response, Request, HTTPError

    def raise_for_status():
        if response.status_code >= 400:
            raise HTTPError

    response = MagicMock(spec=Response)
    response.status_code = 200
    response.raise_for_status = Mock(spec=raise_for_status, side_effect=raise_for_status)

    session_request = MagicMock(spec=Request)
    session_request.response = response
    session_request.return_value = response

    return session_request


@fixture
def patch_requests(monkeypatch, mock_session_request):
    """
    :type monkeypatch: _pytest.monkeypatch.monkeypatch
    :type mock_session_request: mock.MagicMock
    """
    import json

    def pickle_dumps(value):
        obj = {
            'status_code': value.status_code
        }
        return json.dumps(obj)

    def pickle_loads(value):
        try:
            value_string = value.decode("utf-8")
        except AttributeError:
            value_string = str(value)

        obj = json.loads(value_string)
        mock_session_request.response.status_code = obj.get('status_code')
        return mock_session_request

    monkeypatch.setattr('cache_requests._compat.pickle.dumps', pickle_dumps)
    monkeypatch.setattr('cache_requests._compat.pickle.loads', pickle_loads)
    monkeypatch.setattr('requests.sessions.Session.request', mock_session_request)


@fixture
def requests():
    from cache_requests.sessions import Session

    return Session()


@mark.usefixtures('patch_requests')
def test_requests_get(requests, mock_session_request):
    """
    :type requests: cache_requests.sessions.Session
    :type mock_session_request: mock.MagicMock
    """

    mock_session_request.assert_not_called()
    # 1st unique call
    requests.get('http://google.com')
    assert mock_session_request.call_count == 1
    requests.get('http://google.com')
    requests.get('http://google.com')
    assert mock_session_request.call_count == 1

    headers = {
        "accept-encoding": "gzip, deflate, sdch",
        "accept-language": "en-US,en;q=0.8"
    }
    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
                   q="hash%20a%20dictionary%20python")
    # 2nd unique call
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert mock_session_request.call_count == 2
    requests.get('http://google.com/search', headers=headers, params=payload)
    requests.get('http://google.com/search', headers=headers, params=payload)
    requests.get('http://google.com/search', headers=headers, params=payload)
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert mock_session_request.call_count == 2

    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
                   q="hash%20a%20dictionary%20python2")
    # 3rd unique call
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert mock_session_request.call_count == 3
    requests.get('http://google.com/search', headers=headers, params=payload)
    assert mock_session_request.call_count == 3


@mark.usefixtures('patch_requests')
def test_requests_options(requests, mock_session_request):
    """
    :type requests: cache_requests.sessions.Session
    :type mock_session_request: mock.MagicMock
    """

    mock_session_request.assert_not_called()
    requests.options('http://google.com')
    requests.options('http://google.com')
    assert mock_session_request.call_count == 1
    assert mock_session_request.call_args == (('OPTIONS', 'http://google.com'), dict(allow_redirects=True))


@mark.usefixtures('patch_requests')
def test_requests_head(requests, mock_session_request):
    """
    :type requests: cache_requests.sessions.Session
    :type mock_session_request: mock.MagicMock
    """

    mock_session_request.assert_not_called()
    requests.head('http://google.com')
    requests.head('http://google.com')
    assert mock_session_request.call_count == 1

    assert mock_session_request.call_args == (('HEAD', 'http://google.com'), dict(allow_redirects=False))


@mark.usefixtures('patch_requests')
def test_requests_post(requests, mock_session_request):
    """
    :type requests: cache_requests.sessions.Session
    :type mock_session_request: mock.MagicMock
    """

    requests.cache.post = True

    mock_session_request.assert_not_called()
    requests.post('http://google.com')
    requests.post('http://google.com')
    assert mock_session_request.call_count == 1
    mock_session_request.assert_called_with('POST', 'http://google.com', data=None, json=None)


@mark.usefixtures('patch_requests')
def test_requests_put(requests, mock_session_request):
    """
    :type requests: cache_requests.sessions.Session
    :type mock_session_request: mock.MagicMock
    """

    requests.cache.put = True

    mock_session_request.assert_not_called()
    requests.put('http://google.com')
    requests.put('http://google.com')
    assert mock_session_request.call_count == 1
    mock_session_request.assert_called_with('PUT', 'http://google.com', data=None)


@mark.usefixtures('patch_requests')
def test_requests_patch(requests, mock_session_request):
    """
    :type requests: cache_requests.sessions.Session
    :type mock_session_request: mock.MagicMock
    """

    requests.cache.patch = True

    mock_session_request.assert_not_called()
    requests.patch('http://google.com')
    requests.patch('http://google.com')
    assert mock_session_request.call_count == 1
    mock_session_request.assert_called_with('PATCH', 'http://google.com', data=None)


@mark.usefixtures('patch_requests')
def test_requests_delete(requests, mock_session_request):
    """
    :type requests: cache_requests.sessions.Session
    :type mock_session_request: mock.MagicMock
    """

    requests.cache.delete = True

    mock_session_request.assert_not_called()
    requests.delete('http://google.com')
    requests.delete('http://google.com')
    assert mock_session_request.call_count == 1
    mock_session_request.assert_called_with('DELETE', 'http://google.com')


@mark.usefixtures('patch_requests')
def test_memoize_toggled_off(requests, mock_session_request):
    """
    :type requests: cache_requests.sessions.Session
    :type mock_session_request: mock.MagicMock
    """

    requests.cache.get = False

    mock_session_request.assert_not_called()
    requests.get('http://google.com')
    requests.get('http://google.com')
    assert mock_session_request.call_count == 2


@mark.usefixtures('patch_requests')
def test_only_cache_200_response(requests, redis_mock, mock_session_request):
    """
    :type requests: cache_requests.sessions.Session
    :type mock_session_request: mock.MagicMock
    :type redis_mock: mock.MagicMock
    """
    # LOCAL TEST HELPER
    # ------------------------------------------------------------------------
    def call_count():
        try:
            return redis_mock.get.call_count, redis_mock.set.call_count
        finally:
            redis_mock.reset_mock()

    # LOCAL SETUP
    # ------------------------------------------------------------------------
    requests.connection = redis_mock

    # TEST SETUP
    # ------------------------------------------------------------------------
    redis_mock.assert_not_called()
    assert call_count() == (0, 0)

    requests.get('http://google.com')  # 1 get, 1 set
    requests.get('http://google.com')  # 1 get, 0 sets

    assert call_count() == (2, 1)

    # TEST 404 RESPONSE DOES NOT CACHE
    # ------------------------------------------------------------------------
    mock_session_request.response.status_code = 404

    requests.get('http://google.com', bust_cache=True)  # 0 gets, 0 sets
    requests.get('http://google.com')  # 1 get, 0 set

    assert call_count() == (1, 0)

    # TEST 200 RESPONSE DOES CACHE
    # ------------------------------------------------------------------------
    mock_session_request.response.status_code = 200

    requests.get('http://google.com')  # 1 get, 1 set
    requests.get('http://google.com')  # 1 get, 0 sets

    assert call_count() == (2, 1)


def test_redis_getter_setter(tmpdir):
    """:type tmpdir: py.path.local"""
    
    from cache_requests import Session
    from redislite import StrictRedis

    # LOCAL SETUP
    # ------------------------------------------------------------------------
    request = Session()

    test_db = tmpdir.join('test_redis.db').strpath
    test_connection = request.connection
    alt_db = tmpdir.join('test_redis_getter_setter.db').strpath
    alt_connection = StrictRedis(dbfilename=alt_db)

    # TEST SETUP
    # ------------------------------------------------------------------------
    assert test_connection.db == test_db
    assert alt_connection.db == alt_db
    assert test_db != alt_db

    # TEST SESSION CONNECTION IDENTITY WITH METHOD's REDIS HANDLE
    # ------------------------------------------------------------------------

    assert request.get.redis is request.connection
    assert request.connection.db == test_db

    request.post.redis = alt_connection

    assert request.post.redis is request.patch.redis
    assert request.post.redis is request.connection
    assert request.post.redis.db == alt_db

    request.connection = test_connection

    assert request.delete.redis is request.patch.redis
    assert request.delete.redis is request.connection
    assert request.delete.redis.db == test_db
