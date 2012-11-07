import os
from functools import wraps
from argparse import ArgumentParser
from fabric.context_managers import prefix


def cached_property(func):
    cach_attr = '_{0}'.format(func.__name__)

    @property
    def wrap(self):
        if not hasattr(self, cach_attr):
            value = func(self)
            if value is not None:
                setattr(self, cach_attr, value)
        return getattr(self, cach_attr, None)
    return wrap


def cli(*args, **kwargs):
    def decorator(func):
        class Parser(ArgumentParser):
            def handle(self, *args, **kwargs):
                try:
                    func(*args, **kwargs)
                except Exception, e:
                    self.error(e.message)

            # No catching of exceptions
            def handle_raw(self, *args, **kwargs):
                func(*args, **kwargs)

        return Parser(*args, **kwargs)
    return decorator


def virtualenv(path):
    "Wraps a function and prefixes the call with the virtualenv active."
    if path is None:
        activate = None
    else:
        activate = os.path.join(path, 'bin/activate')

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if path is not None:
                with prefix('source {0}'.format(activate)):
                    func(*args, **kwargs)
            else:
                func(*args, **kwargs)
        return inner
    return decorator
