import logging
import sys
import time
from functools import wraps

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def wrapper(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        func_name = func.__name__
        logging.debug(f'{func_name} executed in {end - start:.8f} seconds.')
        return result
    return wrapped
