=====
Usage
=====

To use cache_requests in a project::

    import cache_requests

Quick Start
-----------

To use ``cache_requests`` in a project::

    >>> from cache_requests import Session()

    requests = Session()

    # from python-requests.org
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


Config Options
--------------

Decorated Methods
~~~~~~~~~~~~~~~~~

``method.ex``
    sets the default expiration (seconds) for new cache entries.

``method.redis``
    creates the connection to the ``redis`` or ``redislite`` database. By default this is a ``redislite`` connection. However, a redis connection can be dropped in for easy scalability.


:mod:`cache_requests.Session`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``ex`` and ``redis`` are shared between request methods.  They can be accessed by ``Session.ex`` or ``Session.get.ex``, where ``get`` is the ``requests.get`` method

- By default requests that return and error will not be cached.  This can be overridden by overriding the ``Session.set_cache_cb`` to return ``False``.  The callback takes the response object as an argument::

        from cache_requests import Session

        requests = Session()

        requests.set_cache_db = lambda _:False

- By default only autonomous methods are cached (``get``, ``head``, ``options``).  Each method can be setup to be cached using the ``Session.cache`` config option.



These methods are accessed through the Session objects ``Session.cache.[method name]``.
They can be overridden with the ``Session.cache.all`` setting.

For example::

        from cache_requests import Session

        requests = Session()

        requests.cache.delete = True

        # cached, only called once.
        requests.delete('http://google.com')
        requests.delete('http://google.com')

        requests.cache.delete = True

        # not cached, called twice.
        requests.delete('http://google.com')
        requests.delete('http://google.com')

        # cache ALL methods
        requests.cache.all = True

        # don't cache any methods
        requests.cache.all = False

        # Use individual method cache options.
        requests.cache.all = None

Default settings
****************
===========  ========
Method       Cached
===========  ========
``get``      ``True``
``head``     ``True``
``options``  ``True``
``post``     ``False``
``put``      ``False``
``patch``    ``False``
``delete``   ``False``
``all``      ``None``
===========  ========

Function Level Config
~~~~~~~~~~~~~~~~~~~~~

Cache Busting
    Use keyword ``bust_cache=True`` in a memoized function to force reevaluation.

Conditionally Set Cache
    Use keyword ``set_cache`` to provide a callback.  The callback takes the results of function as an argument and must return a ``bool``. Alternatively, ``True`` and ``False`` can be used.

Use Case Scenarios
------------------


Development: 3rd Party APIs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scenario:
    Working on a project that uses a 3rd party API or service.

Things you want:
    * A cache that persists between sessions and is lightning fast.
    * Ability to rapidly explore the API and it's parameters.
    * Ability to inspect and debug response content.
    * Ability to focus on progress.
    * Perfect transition to a production environment.



Things you don't want:
    * Dependency on network and server stability for development.
    * Spamming the API.  Especially APIs with limits.
    * Responses that change in non-meaningful ways.
    * Burning energy with copypasta or fake data to run piece of your program.
    * Slow. Responses.

Make a request one time. Cache the results for the rest of your work session.::

    import os

    if os.environ.get('ENV') == 'DEVELOP':
        from cache_requests import Session

        ex = 60 * 60  # Set expiration, 60 min
        request = Session(ex=ex)
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



Production: Web Scraping
~~~~~~~~~~~~~~~~~~~~~~~~

Automatically expire old content.

    * How often? After a day? A week? A Month? etc.  100% of this logic is built in with the ``Session.ex`` setting.
    * Effectively it can manage all of the time-based rotation.
    * Perfect if you theres more data then what your API caps allow.

One line of code to use a ``redis`` full database.

    * Try ``redislite``; it can handle quite a bit.  The ``redislite`` api used by this module is 1:1 with the redis package.  Just replace the connection parameter/config value.
    * ``redis`` is a drop in:::

        connection  = redis.StrictRedis(host='localhost', port=6379, db=0)
        requests = Session(connection=connection)

    * Everything else just works.  There's no magic required.::

        from cache_requests import Session

        connection  = redis.StrictRedis(host='localhost', port=6379, db=0)
        ex = 7 * 24 * 60 * 60 # 1 week

        requests = Session(ex=ex, connection=connection)

        for i in range(1000)
            payload = dict(q=i)
            response = requests.get('http://google.com/search', params=payload)
            print(response.text)




Usage: memoize
~~~~~~~~~~~~~~

::

    from cache_requests import Memoize

    @Memoize(ex=15 * 60)  # 15 min, default, 60 min
    def amazing_but_expensive_function(*args, **kwargs)
        print("You're going to like this")
