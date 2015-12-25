#!/usr/bin/env python
# coding=utf-8
from cache_requests import Memoize


@Memoize
def expensive_function(*args, **kwargs):
    text = """
    Only prints once!
    Note: Don't cache functions with side effects.
    """
    print(text)

    return args, kwargs


print(expensive_function)
print(expensive_function)
