"""
values.py: Value generators for common proto types
"""

def integral_value_gen():
    for v in [0, 1, -1, 127, -128, 0x7FFFFFFF, -0x80000000, 42]:
        yield v

def float32_value_gen():
    for v in [0.0, 1.0, -1.0, 1e30, -1e30, float('inf'), float('-inf'), 3.14159]:
        yield v

def string_value_gen():
    for v in ["", "a", "abc", "\x00", "特殊字符", "☃"]:
        yield v