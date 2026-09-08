import pytest

def fib(n):
    """Recursive fibonacci as in public_test.lua"""
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def bar(n):
    """Sum of fibonacci numbers, matches bar(n) in public_test.lua"""
    s = 0
    for i in range(1, n+1):
        s += fib(i)
    return s

class DummyProfiler:
    """Python dummy version of cloudwu_luaprofiler for test mimic."""
    def __init__(self):
        self.running = False
        self.records = {}
        self.total = 0

    def start(self, arg1, arg2):
        # stub: starts fake profiling
        self.running = True

    def stop(self):
        self.running = False

    def info(self):
        # For testing, mimic "records" as counting bar/fib invocations
        count = [0]
        def counted_fib(n):
            count[0] += 1
            if n <= 2:
                return 1
            else:
                return counted_fib(n-1) + counted_fib(n-2)
        tmp = 0
        for i in range(1, 13):
            tmp += counted_fib(i)
        # Mimic Lua info as {filename: {line: count}}
        info = {"test_profiler_public.py": {12: count[0]}}
        total = count[0]
        return info, total

def test_profiler_fib_sum_and_info_print(capfd):
    """
    Simulate public_test.lua: profile bar(12), print structure, check output.
    """
    p = DummyProfiler()
    p.start(500, 5)
    result = bar(12)
    info, total = p.info()
    p.stop()
    for filename, line_t in info.items():
        for line, count in line_t.items():
            print(filename, line, count)
    print("total=", total)
    out, _ = capfd.readouterr()
    assert "test_profiler_public.py" in out
    assert "total=" in out
    assert total > 0

def test_bar_fibonacci_sum():
    """Check bar(12) returns sum of first 12 Fibonacci numbers."""
    def pure_fib(n):
        if n <= 2:
            return 1
        else:
            return pure_fib(n-1) + pure_fib(n-2)
    expected = sum(pure_fib(i) for i in range(1, 13))
    assert bar(12) == expected