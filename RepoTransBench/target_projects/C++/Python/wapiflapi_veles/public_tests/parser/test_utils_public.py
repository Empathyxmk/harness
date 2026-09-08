import pytest

# Minimal replacement versions for testing public swapEndian and reverseBytes logic
def swap_endian(u: int, byte_count: int) -> int:
    b = u.to_bytes(byte_count, "little")
    return int.from_bytes(b, "big")

def test_swap_endian_uint16():
    val = 0xABCD
    swapped = swap_endian(val, 2)
    assert swapped == 0xCDAB

def test_swap_endian_uint32():
    val = 0x01234567
    swapped = swap_endian(val, 4)
    assert swapped == 0x67452301

def reverse_bytes(data):
    left, right = 0, len(data) - 1
    while left < right:
        data[left], data[right] = data[right], data[left]
        left += 1
        right -= 1

def test_reverse_bytes():
    data = [9, 8, 7, 6, 5]
    reverse_bytes(data)
    assert data == [5, 6, 7, 8, 9]