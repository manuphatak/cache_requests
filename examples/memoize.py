#!/usr/bin/env python
# coding=utf-8
"""
Instructions:

.. code-block:: shell

    $ make install
    $ python examples/memoize.py


Demonstrates:

- How to memoize functions
- How each instance is configured uniquely
- How to set expiration timer.

Sample output below.
"""
from __future__ import print_function
from cache_requests import Memoize


@Memoize
def expensive_function(*args, **kwargs):
    text = """
    Only prints once, even from multiple program runs!
    Note: Don't cache functions with side effects.
    """
    print(text)

    return args, kwargs


@Memoize(ex=3)  # 3 seconds
def shorter_expiration(*args, **kwargs):
    text = """
    Still prints only once every few seconds.
    """
    print(text)

    return expensive_function(*args, **kwargs)

print('1:',end=' ')
print(expensive_function('any', 42, 'combinations', of='args', and_='kwargs'))
print('2:',end=' ')
print(expensive_function('any', 42, 'combinations', of='args', and_='kwargs'))
print('3:',end=' ')
print(shorter_expiration('any', 42, 'combinations', of='args', and_='kwargs'))
print('4:',end=' ')
print(shorter_expiration('any', 42, 'combinations', of='args', and_='kwargs'))

"""
Sample output, several runs:

.. code-block:: sh-session


    $ python examples/memoize.py
    1:
        Only prints once, even from multiple program runs!
        Note: Don't cache functions with side effects.

    (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})
    2: (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})
    3:
        Still prints only once every few seconds.

    (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})
    4: (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})

    $ python examples/memoize.py
    1: (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})
    2: (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})
    3: (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})
    4: (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})

    $ python examples/memoize.py
    1: (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})
    2: (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})
    3:
        Still prints only once every few seconds.

    (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})
    4: (('any', 42, 'combinations'), {'and_': 'kwargs', 'of': 'args'})

    $ python examples/memoize.py
    1: (('any', 42, 'combinations'), {'of': 'args', 'and_': 'kwargs'})
    2: (('any', 42, 'combinations'), {'of': 'args', 'and_': 'kwargs'})
    3: (('any', 42, 'combinations'), {'of': 'args', 'and_': 'kwargs'})
    4: (('any', 42, 'combinations'), {'of': 'args', 'and_': 'kwargs'})



"""
