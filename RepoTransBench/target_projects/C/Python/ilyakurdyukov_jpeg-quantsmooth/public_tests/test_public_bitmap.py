import pytest
import struct

class PublicBitmap:
    """
    Minimal bitmap_t struct equivalent and functions for testing purposes,
    mirroring the implementation in public_test_bitmap.c with its specific logic.
    """
    def __init__(self, width=0, height=0, bpp=0, stride=0, data_size=0):
        self.width = width
        self.height = height
        self.bpp = bpp
        self.stride = stride
        # In C, data points to memory directly after the struct.
        # In Python, we just conceptualize the allocated size.
        self.data_size = data_size

    @staticmethod
    def create(width, height, bpp):
        if width <= 0 or height <= 0 or bpp <= 0:
            return None
        if width > 9000 or height > 9000: # Different limit than original test
            return None

        # Simulate stride calculation as in public_test_bitmap.c
        # (width * bpp + 7) & -4 effectively rounds (width * bpp + 7) down to the nearest multiple of 4.
        # This has the effect of rounding width*bpp up to the next multiple of 4, but with an offset.
        # e.g., if width*bpp = 1, (1+7)&-4 = 8. If width*bpp = 4, (4+7)&-4 = 8. If width*bpp = 5, (5+7)&-4 = 12.
        stride = (width * bpp + 7) & ~3 # ~3 is -4 in two's complement for typical 32-bit int

        # Simulate single allocation for bitmap_t and data
        # In C: size_t size = sizeof(bitmap_t) + stride * height;
        # Python doesn't need to allocate like this, but we store the conceptual size.
        # We need a dummy size for the PublicBitmap object itself to match C's sizeof(bitmap_t)
        # Python's `sys.getsizeof` gives object size, but for testing C struct size we'll use a fixed value.
        # Let's assume sizeof(bitmap_t) is 24 bytes (4 ints + 1 ptr).
        sizeof_bitmap_t_sim = 24
        total_data_bytes = stride * height
        conceptual_total_size = sizeof_bitmap_t_sim + total_data_bytes

        # In Python, we just create the object, no manual malloc simulation needed for success path
        # But we will check if it conceptually would have failed due to memory.
        # If total_data_bytes is extremely large, Python might still succeed, but C would fail.
        # We don't simulate malloc failure beyond the explicit width/height limits.

        bm = PublicBitmap()
        bm.width = width
        bm.height = height
        bm.bpp = bpp
        bm.stride = stride
        bm.data_size = total_data_bytes # Conceptual size of data buffer

        return bm

    @staticmethod
    def free(bm):
        # In Python, memory is managed by garbage collection.
        # This function is a no-op but included to match the C interface conceptually.
        if bm is not None:
            pass # Python's GC will handle deallocation

def test_bitmap_create_valid_newdata():
    """
    Corresponds to START_TEST(test_bitmap_create_valid_newdata) in C.
    """
    width = 10
    height = 6
    bpp = 2
    bm = PublicBitmap.create(width, height, bpp)
    assert bm is not None
    assert bm.width == width
    assert bm.height == height
    assert bm.bpp == bpp

    # Validate stride is multiple of 4 and at least width * bpp
    expected_min_stride = width * bpp
    assert bm.stride >= expected_min_stride
    assert bm.stride % 4 == 0
    PublicBitmap.free(bm)

def test_bitmap_create_invalid_zero():
    """
    Corresponds to START_TEST(test_bitmap_create_invalid_zero) in C.
    """
    bm = PublicBitmap.create(0, 2, 3) # width zero
    assert bm is None
    bm = PublicBitmap.create(1, 0, 3) # height zero
    assert bm is None
    bm = PublicBitmap.create(5, 1, 0) # bpp zero
    assert bm is None

def test_bitmap_create_large_outofrange():
    """
    Corresponds to START_TEST(test_bitmap_create_large_outofrange) in C.
    """
    bm = PublicBitmap.create(9001, 10, 1) # exceeds public test limit (9000)
    assert bm is None
    bm = PublicBitmap.create(10, 9002, 1) # exceeds public test limit (9000)
    assert bm is None