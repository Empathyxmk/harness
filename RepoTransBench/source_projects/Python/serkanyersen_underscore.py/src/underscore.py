import random as _random

def chunk(lst, n):
    """Split a list into chunks of size n."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def compact(lst):
    """Remove falsy values from a list."""
    return [x for x in lst if x]

def identity(val):
    """Returns the value passed as an argument."""
    return val

def map_(lst, fn):
    """Apply function to each element of list."""
    return [fn(x) for x in lst]

def once(fn):
    """Return a function that only runs fn once."""
    result = []
    called = [False]
    def wrapper(*args, **kwargs):
        if not called[0]:
            called[0] = True
            value = fn(*args, **kwargs)
            result.append(value)
        return result[0]
    return wrapper

def is_empty(value):
    """Check if a collection is empty."""
    if hasattr(value, '__len__'):
        return len(value) == 0
    return not bool(value)

def keys(d):
    """Return the keys of a dictionary."""
    return list(d.keys())

def pairs(d):
    """Return (key, value) pairs of a dictionary."""
    return list(d.items())

def random(a, b):
    """Return a random integer between a and b inclusive."""
    return _random.randint(a, b)