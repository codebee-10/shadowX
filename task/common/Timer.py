import time
from functools import wraps


def timer(function):
    """
    :param function:
    :return: 装饰器实现一个计时器
    """
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" % (function.func_name, str(t1-t0)))
        return result
    return function_timer


class Timer(object):
    """
    上下文管理器实现一个计时器
    """

    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # 毫秒
        if self.verbose:
            print('elapsed time: %f ms' % self.msecs)


if __name__ == '__main__':

    def fib(n):
        if n in [1, 2]:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)

    with Timer(True):
        print(fib(30))
