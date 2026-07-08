import time

from functools import wraps


def monitor(metric):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start = time.perf_counter()

            try:

                return func(*args, **kwargs)

            finally:

                metric.observe(time.perf_counter() - start)

        return wrapper

    return decorator
