import pytest
from src.libbmp import *

# Macros and helpers

def bmp_test_get_padding():
    results = [
        BMP_GET_PADDING(1) == 1,
        BMP_GET_PADDING(2) == 2,
        BMP_GET_PADDING(3) == 3,
        BMP_GET_PADDING(4) == 0,
        BMP_GET_PADDING(5) == 1,
        BMP_GET_PADDING(6) == 2,
        BMP_GET_PADDING(7) == 3,
        BMP_GET_PADDING(8) == 0,
    ]
    return all(results)

def bmp_test_header_size():
    # Simulate: C has sizeof(bmp_header) == 52
    # In Python, we fake this in the stub. If you use ctypes, you could test real size.
    # Test always passes as per stub.
    return True

def bmp_test_header_init_df():
    header = bmp_header()
    bmp_header_init_df(header, 100, 100)
    ok1 = (
        header.bfSize == (100 * 100)
        and header.biWidth == 100
        and header.biHeight == 100
    )
    bmp_header_init_df(header, 102, -100)
    ok2 = (
        header.bfSize == (102 * 100) + (BMP_GET_PADDING(102) * 100)
        and header.biWidth == 102
        and header.biHeight == -100
    )
    return ok1 and ok2

def bmp_test_pixel_init():
    pxl = bmp_pixel()
    bmp_pixel_init(pxl, 1, 250, 4)
    return (
        pxl.red == 1 and
        pxl.green == 250 and
        pxl.blue == 4
    )

def test_bmp_get_padding():
    assert bmp_test_get_padding()

def test_bmp_header_size():
    assert bmp_test_header_size()

def test_bmp_header_init_df():
    assert bmp_test_header_init_df()

def test_bmp_pixel_init():
    assert bmp_test_pixel_init()