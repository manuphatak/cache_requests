#!/usr/bin/env python
# coding=utf-8
"""
cache_requests
--------------

This module implements a basic LRU decorator that syncs calls with a redislite database.

ELI5:  If you call the same function with the same parameters, it does not recalculate
    the function.  Instead, the first time, the results are stored, the second time the
    results are retrieved from storage.

    It gets worse.  Unlike a regular LRU cache, this storage survives after the program
    finishes. It's destroyed based on an expiration timer.

EXPIRATION: (int) Keys are destroyed in this amount of time.  Can be set to None
"""
import copy
import cPickle as pickle

import requests
import redislite


try:
    # hook into project logger
    from log import set_up_log

    log = set_up_log(__name__)
except ImportError:
    import logging as log

    format_ = '%(relativeCreated)-5d %(name)-12s %(levelname)-8s %(message)s'
    log.basicConfig(level=log.DEBUG, format=format_)

EXPIRATION = 1 * 60 * 60  # 1 hour

redis_connection = redislite.StrictRedis(dbfilename='redis/requests.redis')


def make_hash(obj):
    """
    Recursively hash nested mixed objects (dicts, lists, other).
    """
    if isinstance(obj, (set, tuple, list)):
        return tuple(make_hash(item) for item in obj if item)
    elif not isinstance(obj, dict):
        return hash(obj)

    copied_obj = copy.deepcopy(obj)
    for k, v in copied_obj.items():
        copied_obj[k] = make_hash(v)

    return hash(tuple(frozenset(sorted(copied_obj.items()))))


class Memoize(object):
    """
    Decorator.  Standard LRU PLUS get/set keys with redis.
    """

    def __init__(self, function):
        self.redis = redis_connection
        self.function = function

    def __getitem__(self, item):
        try:
            return pickle.loads(self.redis.get(item))
        except TypeError:
            return False  # Key was not found

    def __setitem__(self, key, value):
        self.redis.set(name=key, value=pickle.dumps(value), ex=EXPIRATION)

    def __call__(self, *args, **kwargs):
        memo_key = make_hash((args, kwargs))
        if not self[memo_key]:
            self[memo_key] = self.function(*args, **kwargs)
            log.info('Caching results for hash: %s ', memo_key)
        else:
            log.debug('Results from cache hash: %s', memo_key)
        return self[memo_key]

# monkeypatch + decorate requests library
requests.get = Memoize(requests.get)
requests.post = Memoize(requests.post)

if __name__ == '__main__':
    # demonstration
    EXPIRATION = 15  # 15 seconds

    # 1st unique call
    response = requests.get('http://google.com')
    response = requests.get('http://google.com')
    response = requests.get('http://google.com')

    headers = {"accept-encoding": "gzip, deflate, sdch",
               "accept-language": "en-US,en;q=0.8"}
    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8",
                   client="ubuntu", q="hash%20a%20dictionary%20python")
    # 2nd unique call
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)

    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8",
                   client="ubuntu", q="hash%20a%20dictionary%20python2")
    # 3rd unique call
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)

    print(response.text)

    # Pay attention to the number of requests made.   Even though there are 10
    # `requests.get`s, there's only 3 requests being sent out.

    # Now run it again within 15 seconds.

    # This time there was 0 unique `requests.get`s.  It pulls 100% from cache.

    # Wait 15 seconds, and run it one last time.  Now that those keys have expired it
    # will resend those requests and repopulate the cache storage.

    # One more thing, you may notice.  It runs almost 10x faster when it's not sending
    # requests.