""" func.py - Additional tools for working with functions and callable objects
"""

__all__ = ['persistent_cache']

import functools

from .collections import PersistentDict


def _map_wrapper(user_func, m):

    @functools.wraps(user_func)
    def wrapper(*args, **kwargs):
        key = args + tuple(kwargs.items())
        if key in m:
            return m[key]
        response = user_func(*args, **kwargs)
        m[key] = response
        return response

    return wrapper


def persistent_cache(identifier=None, **kwargs):
    def decorator(user_func):
        pm = PersistentDict(
            identifier if identifier else user_func.__name__,
            **kwargs)
        return _map_wrapper(user_func, pm)

    return decorator
