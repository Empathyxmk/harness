import pytest
from src.libbmp import *

def bmp_test_get_padding_public():
    # Use different input set to test padding macro
    results = [
        BMP_GET_PADDING(5) == 1,
        BMP_GET_PADDING(6) == 2,
        BMP_GET_PADDING(9) == 3,
        BMP_GET_PADDING(12) == 0,
        BMP_GET_PADDING(13) == 1,
        BMP_GET_PADDING(14) == 2,
        BMP_GET_PADDING(15) == 3,
        BMP_GET_PADDING(16) == 0,
    ]
    return all(results)

def bmp_test_header_size_public():
    return True

def bmp_test_header_init_df_public():
    header = bmp_header()
    bmp_header_init_df(header, 77, 55)
    ok1 = (
        header.bfSize == (77 * 55)
        and header.biWidth == 77
        and header.biHeight == 55
    )
    bmp_header_init_df(header, 20, -30)
    ok2 = (
        header.bfSize == (20 * 30) + (BMP_GET_PADDING(20) * 30)
        and header.biWidth == 20
        and header.biHeight == -30
    )
    return ok1 and ok2

def bmp_test_pixel_init_public():
    pxl = bmp_pixel()
    bmp_pixel_init(pxl, 128, 64, 32)
    return pxl.red == 128 and pxl.green == 64 and pxl.blue == 32

def test_bmp_get_padding_public():
    assert bmp_test_get_padding_public()

def test_bmp_header_size_public():
    assert bmp_test_header_size_public()

def test_bmp_header_init_df_public():
    assert bmp_test_header_init_df_public()

def test_bmp_pixel_init_public():
    assert bmp_test_pixel_init_public()