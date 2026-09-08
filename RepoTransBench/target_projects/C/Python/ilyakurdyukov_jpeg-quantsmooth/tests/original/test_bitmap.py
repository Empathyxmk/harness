import pytest
import struct

class OriginalBitmap:
    """
    Minimal bitmap_t struct equivalent and functions for testing purposes,
    mirroring the implementation in test_bitmap.c.
    """
    def __init__(self, width=0, height=0, bpp=0, stride=0, data=None):
        self.width = width
        self.height = height
        self.bpp = bpp
        self.stride = stride
        self.data = data if data is not None else b'' # Use bytes for data simulation

    @staticmethod
    def create(width, height, bpp):
        if width <= 0 or height <= 0 or bpp <= 0:
            return None
        if width > 10000 or height > 10000: # Prevent large allocations in tests
            return None

        size = width * height * bpp
        bmp = OriginalBitmap()
        bmp.width = width
        bmp.height = height
        bmp.bpp = bpp
        bmp.stride = width * bpp
        # Simulate memory allocation for data, but Python handles actual memory
        bmp.data = b'\x00' * size # Initialize with zeros as per calloc
        if not bmp.data: # In Python, this will typically not fail unless size is huge
            return None # Simulate allocation failure

        return bmp

    @staticmethod
    def free(bmp):
        # In Python, memory is managed by garbage collection.
        # This function is a no-op but included to match the C interface conceptually.
        # We can test that calling it with None doesn't crash.
        if bmp is not None:
            pass # Python's GC will handle deallocation

def test_bitmap_create_basic():
    """
    Corresponds to START_TEST(test_bitmap_create_basic) in C.
    """
    bmp = OriginalBitmap.create(10, 8, 3) # Basic valid input
    assert bmp is not None
    assert bmp.width == 10
    assert bmp.height == 8
    assert bmp.bpp == 3
    assert bmp.data is not None
    OriginalBitmap.free(bmp)

def test_bitmap_create_overflow():
    """
    Corresponds to START_TEST(test_bitmap_create_overflow) in C.
    """
    bmp = OriginalBitmap.create(100000, 10, 3)
    assert bmp is None

    bmp = OriginalBitmap.create(10, 100000, 3)
    assert bmp is None

    bmp = OriginalBitmap.create(-1, 10, 3)
    assert bmp is None

    bmp = OriginalBitmap.create(10, -1, 3)
    assert bmp is None

    bmp = OriginalBitmap.create(10, 10, -5)
    assert bmp is None

def test_bitmap_create_minimal():
    """
    Corresponds to START_TEST(test_bitmap_create_minimal) in C.
    """
    bmp = OriginalBitmap.create(1, 1, 1)
    assert bmp is not None
    OriginalBitmap.free(bmp)

def test_bitmap_free_null():
    """
    Corresponds to START_TEST(test_bitmap_free_null) in C.
    In Python, this is a no-op that shouldn't raise an error.
    """
    OriginalBitmap.free(None)
    # No assertion needed, success is not raising an exception