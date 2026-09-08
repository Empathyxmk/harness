def fib(n, memo=None):
    if memo is None: memo = {}
    if n in memo: return memo[n]
    if n < 2: return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

def test_public_fib_small():
    assert fib(0) == 0
    assert fib(4) == 3
    assert fib(7) == 13