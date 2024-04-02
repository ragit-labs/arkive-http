import asyncio
from functools import wraps


def fire_and_forget(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if callable(func):
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, func, *args, **kwargs)
        else:
            raise TypeError("The argument must be a callable")

    return wrapped
