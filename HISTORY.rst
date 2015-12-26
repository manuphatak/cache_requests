=======
History
=======

Next Release
------------

- Stay tuned.


4.0.0 (2015-12-25)
------------------

- Fix: Use MD5 for hash to avoid PYTHONHASHSEED issue.
- Fix: Give default dbfilename a more unique name, based on caller.
- BREAKING:Move ``Session.ex`` and ``Session.connection`` to ``Session.cache`` config object.
- Updated examples.  New example demonstrates Memoize decorator.
- Updated requirements.

3.0.0 (2015-12-22)
------------------

- Feature: Cache busting! Use keyword argument ``bust_cache=True`` to force reevaluation.
- Feature: Session automatically skips caching error responses.
- Feature: Callback argument to decide if results should be cached.
- Feature: Decorated Session methods share a centralized configuration per session.
- BREAKING: Remove global config, in favor component level config.  Reasoning: Global config adds way too much complexity and adds too little value.  (Everything needs to lazy load the config at the last moment)
- Fix: Unique cache per function in shared db.
- Fix: Tweaks to keep the classes sub classable.
- Fix: Cleaned up tests.
- Updated requirements.

2.0.0 (2015-12-12)
------------------

- API completely rewritten
- New API extends ``requests`` internals as opposed to monkeypatching.
- Entire package is redesigned to be more maintainable, more modular, and more usable.
- Dependencies are pinned.
- Tests are expanded.
- PY26 and PY32 support is dropped, because of dependency constraints.
- PY35 support is added.
- Docs are rewritten.
- Move towards idiomatic code.
- 2.0.6 Fix broken coverage, broken rst render.

1.0.0 (2015-04-23)
------------------

- First real release.
- Feature/ Unit test suite, very high coverage.
- Feature/ ``redislite`` integration.
- Feature/ Documentation.  https://cache-requests.readthedocs.org.
- Feature/ Exposed the beefed up ``Memoize`` decorator.
- Feature/ Upgraded compatibility to:
    - PY26
    - PY27
    - PY33
    - PY34
    - PYPY
- Added examples and case studies.


0.1.0 (2015-04-19)
------------------

- First release on PyPI.
