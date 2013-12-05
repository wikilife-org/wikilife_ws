# coding=utf-8

import functools


def catch_exceptions(method):
    """Decorate RequestHandler methods with this to catch any exceptions and return an informative JSON."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception, e:
            self.error(e)

    return wrapper
