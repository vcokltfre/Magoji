from asyncio import Future, get_event_loop
from functools import partial, wraps
from concurrent.futures import Executor
from typing import Callable, Optional

def run_in_executor(executor: Optional[Executor] = None) -> Callable[..., Future]:

    loop = get_event_loop()

    def decorator(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            func = partial(func, *args, **kwargs)

            return loop.run_in_executor(executor, func)

        return inner

    return decorator
