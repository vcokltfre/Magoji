from asyncio import get_event_loop
from functools import partial, wraps


def run_in_executor(loop=None):

    loop = loop or get_event_loop()

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            func = partial(func, *args, **kwargs)

            return loop.run_in_executor(None, func)

        return inner

    return decorator
