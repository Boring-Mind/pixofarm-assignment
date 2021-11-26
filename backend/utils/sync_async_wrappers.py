import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from typing import Callable


def force_async(fn: Callable):
    """Turns a sync function to async function using threads"""
    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def force_sync(fn: Callable):
    """Turn an async function to sync function"""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper
