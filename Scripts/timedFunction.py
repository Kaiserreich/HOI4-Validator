import functools
import time


def timed(func):
    @functools.wraps(func)
    def timer_wrapper(*args, **kwargs):
        t0 = time.time()
        func(*args, **kwargs)
        t0 = time.time() - t0
        print("Time taken to run " + func.__name__ + " script: " + (t0 * 1000).__str__() + " ms")
    return timer_wrapper