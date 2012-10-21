from argparse import ArgumentParser


def cached_property(func):
    cach_attr = '_{}'.format(func.__name__)

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
