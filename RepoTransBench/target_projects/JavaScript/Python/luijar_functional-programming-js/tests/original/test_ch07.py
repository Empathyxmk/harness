# Memoization tests
def fib(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo: return memo[n]
    if n < 2: return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

def memoize(f):
    cache = {}
    def wrapped(x):
        if x not in cache:
            cache[x] = f(x)
        return cache[x]
    return wrapped

def test_fib_normal():
    assert fib(5) == 5
    assert fib(10) == 55

def test_memoize_functionality():
    calls = []
    def slow(x):
        calls.append(x)
        return x * x
    mslow = memoize(slow)
    assert mslow(2) == 4
    assert mslow(2) == 4  # second call should not re-call original
    assert calls == [2]
    assert mslow(3) == 9
    assert set(calls) == {2,3}