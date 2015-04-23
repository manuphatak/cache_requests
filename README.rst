==============
Cache Requests
==============

.. image:: https://pypip.in/status/cache_requests/badge.svg
    :target: https://pypi.python.org/pypi/cache_requests/
    :alt: Development Status

.. image:: https://travis-ci.org/bionikspoon/cache_requests.svg?branch=develop
    :target: https://travis-ci.org/bionikspoon/cache_requests?branch=develop
    :alt: Build Status

.. image:: https://pypip.in/version/cache_requests/badge.svg
    :target: https://pypi.python.org/pypi/cache_requests
    :alt: Latest Version

.. image:: https://coveralls.io/repos/bionikspoon/cache_requests/badge.svg?branch=develop
    :target: https://coveralls.io/r/bionikspoon/cache_requests?branch=develop
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/cache-requests/badge/?version=latest
    :target: https://readthedocs.org/projects/cache-requests/?badge=latest
    :alt: Documentation Status

------------

.. image:: https://pypip.in/py_versions/cache_requests/badge.svg
    :target: https://pypi.python.org/pypi/cache_requests/
    :alt: Supported Python versions

.. image:: https://pypip.in/implementation/cache_requests/badge.svg
    :target: https://pypi.python.org/pypi/cache_requests/
    :alt: Supported Python implementations

.. image:: https://pypip.in/license/cache_requests/badge.svg
    :target: https://pypi.python.org/pypi/cache_requests/
    :alt: License

**Simple. Powerful. Persistent LRU caching for the requests library.**

Features
--------

* Free software: MIT license
* Documentation: https://cache-requests.readthedocs.org.
* Python version agnostic: tested against Python 2.6, 2.7, 3.3, 3.4, and Pypy

..

* Drop in decorator for the requests library.
* Automatic timer based expiration on stored items (optional).
* Backed by yahoo's powerful ``redislite``.
* Scalable with redis. Optionally accepts a ``redis`` connection.
* Exposes the powerful underlying ``Memoize`` decorator to decorate any function.
* Tested with high coverage.
* Lightweight. Simple logic.
* Lightning fast.

..

* Jump start your development cycle.
* Collect and reuse entire response objects.

Installation
------------

At the command line either via easy_install or pip:

.. code-block:: shell

    $ pip install cache_requests


.. rubric:: Uninstall

.. code-block:: shell

    $ pip uninstall cache_requests

Quick Start
-----------

To use ``cache_requests`` in a project:

.. code-block:: python

    >>> from cache_requests import requests

    # source of following sample: python-requests.org
    >>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    >>> r.status_code
    200
    >>> r.headers['content-type']
    'application/json; charset=utf8'
    >>> r.encoding
    'utf-8'
    >>> r.text
    u'{"type":"User"...'
    >>> r.json()
    {u'private_gists': 419, u'total_private_repos': 77, ...}

Use Case Scenarios
------------------

.. epigraph::

    You never know how people are going to use your code; purposes no one person could ever imagine.  This might be scary to some; it's exciting to me.  In this case, this tool was built for one thing: development. Development with an extremely small allowance on API hits. Now that this tool is taking shape production cases and testing cases are starting to look way more appealing--especially with the free, drop-in conversion to ``redis`` full.  There are unlimited possibilities.

Use Case: Development: 3rd Party APIs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Scenario:
    Working on a project that uses a 3rd party API or service.

Things you want:
    * Ability to rapidly explore the API and it's parameters.
    * Ability to inspect and debug response content.
    * Ability to focus on the actual work.
    * Perfect transition to a production environment.



Things you don't want to be doing:
    * Dealing with networking issues while you're trying to work.
    * Spamming the API.  Especially APIs with limits.
    * Responses that change in non-meaningful ways.
    * Burning energy with copypasta or fake data to run piece of your program.
    * Waiting for responses. Yes, maybe it's only a fraction of a second for a normal request and it will never add up to a meaningful cost.  But it will break your zen every time you run.  And you know what I'm talking about.

Make a request one time. Cache the results for the rest of your work session.

.. code-block:: python

    import os

    if os.environ.get('ENV') == develop:
        from cache_requests import requests, config
        config.REDISLITE_DB = 'redis/requests.redislite'
        config.EXPIRATION = 60 * 60  # 60 min
    else:
        import requests

    # strange, complicated request you might make
    headers = {"accept-encoding": "gzip, deflate, sdch", "accept-language": "en-US,en;q=0.8"}
    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
                   q="hash%20a%20dictionary%20python")
    response = requests.get('http://google.com/search', headers=headers, params=payload)

    # spam to prove a point
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)

    # tweak your query, we're exploring here
    payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
                   q="hash%20a%20dictionary%20python2")
    # do you see what changed? the caching tool did.
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)
    response = requests.get('http://google.com/search', headers=headers, params=payload)


Optionally.  Setup with environment variables.  You're probably already doing this for everything else.

.. code-block:: shell

    $ export ENV=develop
    $ export REDISLITE_DB='redis/requests.redislite' # make sure directory exists
    $ export EXPIRATION=3600 # 1 hour; default


Use Case: Production: Web Scraping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Automatically expire old content.
    * How often? After a day? A week? A Month? etc.  100% of this logic is built in with the ``EXPIRATION`` setting.
    * Effectively it can manage all of the time-based rotation.
    * When is this good? Really good if you have limited hit allowance and need to rotate to collect all the data.
One line of code to use a ``redis`` full database.
    * You might be surprised how much ``redislite`` can handle.
    * Using redis full is a drop in.

    .. code-block:: python

        conf.REDIS_CONNECTION  = redis.StrictRedis(host='localhost', port=6379, db=0)

    * Everything else just works.  There's no magic.  Look at the code, it's really simple stuff.

.. code-block:: python

    from cache_requests import requests, config
    # conf.REDIS_CONNECTION  = redis.StrictRedis(host='localhost', port=6379, db=0)
    # let's use lite for now
    config.REDISLITE_DB = 'redis/requests.redislite'
    config.EXPIRATION = 7 * 24 * 60 * 60 # 1 week, I hope, for my ego :)

    # TODO: get a non-lame example
    for i in range(1000)
        payload = dict(q=i)
        response = requests.get('http://google.com/search', params=payload)
        print(response.text)


Use Case: Testing
~~~~~~~~~~~~~~~~~

Quit doing weird things to mock, pickle, etc your responses.

We do this to freeze the results.  We want our unittests to fail because of our own code and not external factors: network, hardware, website target, etc.

Set ``EXPIRATION`` to ``None`` you'll get the same freeze.

Include the database file with your test resources and everyone on your team can use it.

When your external API/web resource changes. Delete the database, it'll repopulate itself with fresh data.

.. code-block:: python

    from cache_requests import requests, config
    config.REDISLITE_DB = 'redis/requests.redislite'
    config.EXPIRATION = None

    def test_weird_things_here()
        assert requests.get('http://amazing_tool') == 'cache_requests'



Usage: Memoize
~~~~~~~~~~~~~~

Options=Unlimited

# TODO inject amazing imagination

.. code-block:: python

    from cache_requests import Memoize, config
    config.REDISLITE_DB = 'redis/requests.redislite'
    config.EXPIRATION = 15 * 60 # 15 min

    @Memoize
    def amazing_but_expensive_function(*args, **kwargs)
        print("You're going to like this")


Manually decorate requests.

.. code-block:: python

    from cache_requests import Memoize, config
    import requests

    config.REDISLITE_DB = 'redis/requests.redislite'
    config.EXPIRATION = 15 * 60 # 15 min

    requests.get = Memoize(requests.get)
    requests.post = Memoize(requests.post)

    print(requests.get('http://google.com').text[:60])
    # u'<!doctype html><html itemscope="" itemtype="http://schema.or'
