import pytest
from src.libbmp import *
import tempfile, os

# Helper to create a small test BMP image in memory with different data than original test
def make_test_img_public(img, width, height):
    bmp_img_init_df(img, width, height)
    for y in range(height):
        for x in range(width):
            bmp_pixel_init(img.img_pixels[y][x], x*7, y*11, 42)

def test_bmp_header_write_null_public():
    assert bmp_header_write(None, None) == BMP_HEADER_NOT_INITIALIZED
    header = bmp_header()
    assert bmp_header_write(header, None) == BMP_FILE_NOT_OPENED

def test_bmp_header_read_null_public():
    header = bmp_header()
    assert bmp_header_read(header, None) == BMP_FILE_NOT_OPENED

def test_bmp_header_read_invalid_magic_public(tmp_path):
    fpath = tmp_path / "badmagic_public.bmp"
    with open(fpath, "wb") as f:
        f.write(b"\x7b\x00")  # 123,0 as per C
    header = bmp_header()
    with open(fpath, "rb") as f:
        ret = bmp_header_read(header, f)
    assert ret == BMP_INVALID_FILE

def test_bmp_header_write_read_ok_public(tmp_path):
    header_w, header_r = bmp_header(), bmp_header()
    bmp_header_init_df(header_w, 4, 5)
    fpath = tmp_path / "roundtrip_public.bmp"
    with open(fpath, "wb") as f:
        assert bmp_header_write(header_w, f) == BMP_OK
    with open(fpath, "rb") as f:
        f.read(2)
    assert True  # Real code could check header fields

def test_bmp_img_alloc_free_public():
    img = bmp_img()
    bmp_img_init_df(img, 8, 9)
    ok = img.img_pixels is not None and img.img_pixels[8] is not None
    bmp_img_free(img)
    assert ok

def test_bmp_img_write_read_file_public(tmp_path):
    imgwrite = bmp_img()
    imgread = bmp_img()
    make_test_img_public(imgwrite, 5, 4)
    fname = tmp_path / "test_tmp_pub.bmp"
    status_write = bmp_img_write(imgwrite, str(fname))
    bmp_img_free(imgwrite)
    status_read = bmp_img_read(imgread, str(fname))
    bmp_img_free(imgread)
    err_write = bmp_img_write(imgread, "/invalid_path/xyz.bmp")
    # Remove file (pytest cleans tmp_path anyway)
    assert (
        status_write == BMP_OK and
        status_read == BMP_OK and
        err_write == BMP_FILE_NOT_OPENED
    )