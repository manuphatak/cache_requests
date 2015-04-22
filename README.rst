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

**Simple. Powerful. Persistent LRU caching.**

* Free software: MIT license
* Documentation: https://cache-requests.readthedocs.org.

Features
--------

* Drop in wrapper  to decorate requests library.
* Optional expiration timer on stored items.
* Backed by yahoo's powerful ``redislite``.
* Scalable. Optionally accepts a ``redis`` connection.  Take advantage of the full power of ``redis``.
* Exposes the powerful underlying ``@Memoize`` decorator.
* ``@Memoize`` can decorate any function to add persistent storage.  Great for expensive calculations.
* Tested. Covered. Documented. Lightweight. Simple logic. Lightning fast.

Installation
------------

At the command line either via easy_install or pip:

.. code-block:: shell

    $ pip install cache_requests

.. code-block:: shell

    $ easy_install cache_requests

**Uninstall**

.. code-block:: shell

    $ pip uninstall cache_requests

Quick Start
-----------

To use ``cache_requests`` in a project:

.. code-block:: python

    from cache_requests import requests

Use Case: Preface
-----------------

When you publicly release your work you quickly find out it will be used in ways you never imaged.  Scary to some, exciting to me.  In this case, this tool was built for one thing: development, with an extremely small allowance on API hits. But, production cases and testing cases are starting to look way more appealing--especially with the free, drop-in conversion to ``redis`` full.  Really, these cases are limited to our collective imagination.

Use Case: Development
---------------------

Make a request one time. Cache the results for the rest of your work session.

* Stop doing weird things. Like pickling and copypasta while you work.
* Change the requests parameters as you figure what you want.  It'll make ONE new request and save the results. ONE total, until it expires (which could be never if you want).
* Don't want caching for production? No problem.
* Tired of waiting entire milliseconds for your requests results? With google.com ``cache_requests`` local cache is about 10x faster, for slower sites this could be much faster.
* Need to strike a strange balance between API key usage and frequently updated results?  No Problem, set the expiration to 5 seconds.

Optional.  Setup with environment variables.  As you likely already are for everything else.

.. code-block:: shell

    $ export ENV=develop
    $ export REDISLITE_DB='redis/requests.redislite' # make sure directory exists
    $ export EXPIRATION=3600 # 1 hour; default

Alternatively setup inline with the ``.config.`` submodule.

.. code-block:: python

    import os

    if os.environ.get('ENV') == develop:
        from cache_requests import requests, config
        config.REDISLITE_DB = 'redis/requests.redislite' # skip if set
        config.EXPIRATION = 60 * 60  # 60 min; skip if set
    else:
        import requests # production or testing

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




Use Case: Production: Web Scraping
----------------------------------

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
-----------------

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



Usage: @Memoize
---------------

Options=Unlimited
# TODO limit the options with lame imagination

.. code-block:: python

    from cache_requests import Memoize, config
    config.REDISLITE_DB = 'redis/requests.redislite'
    config.EXPIRATION = 15 * 60 # 15 min

    @Memoize
    def amazing_but_expensive_function(*args, **kwargs)
        print("You're going to like this")