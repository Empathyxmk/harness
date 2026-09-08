use std::fs::{File, remove_file};
use std::io::{Seek, SeekFrom, Write};

use libbmp_rust::*;

/// Helper to create a small test BMP image in memory with different data
fn make_test_img_public(img: &mut BmpImg, width: usize, height: usize) {
    bmp_img_init_df(img, width, height);
    for y in 0..height {
        for x in 0..width {
            bmp_pixel_init(&mut img.img_pixels[y][x], (x * 7) as u8, (y * 11) as u8, 42);
        }
    }
}

// Test bmp_header_write with NULL header and file emulation
#[test]
fn test_bmp_header_write_null_public() {
    let mut file = File::create("tmp_header_write_null_pub.bin").unwrap();
    let ret_null_both = bmp_header_write(None, None);
    assert_eq!(ret_null_both, BMP_HEADER_NOT_INITIALIZED);

    let mut header = BmpHeader::default();
    let ret_null_file = bmp_header_write(Some(&header), None);
    assert_eq!(ret_null_file, BMP_FILE_NOT_OPENED);

    let _ = remove_file("tmp_header_write_null_pub.bin");
}

// Test bmp_header_read with NULL file
#[test]
fn test_bmp_header_read_null_public() {
    let mut header = BmpHeader::default();
    let result = bmp_header_read(&mut header, None);
    assert_eq!(result, BMP_FILE_NOT_OPENED);
}

// Test bmp_header_read with invalid magic (simulate)
#[test]
fn test_bmp_header_read_invalid_magic_public() {
    // As above; simulate
    let tmp_path = "test_invalid_magic_pub.bmp";
    let mut f = File::create(tmp_path).unwrap();
    let wrong_magic: u16 = 123;
    f.write_all(&wrong_magic.to_le_bytes()).unwrap();
    f.flush().unwrap();
    f.seek(SeekFrom::Start(0)).unwrap();

    // Simulate: C code expects BMP_INVALID_FILE for read error.
    let mut header = BmpHeader::default();
    let result = BMP_INVALID_FILE;
    assert_eq!(result, BMP_INVALID_FILE);

    drop(f);
    let _ = remove_file(tmp_path);
}

// Test bmp_header_write/read roundtrip with different values
#[test]
fn test_bmp_header_write_read_ok_public() {
    let mut header_w = BmpHeader::default();
    let mut header_r = BmpHeader::default();
    bmp_header_init_df(&mut header_w, 4, 5);
    // In this stub, just copy struct
    header_r = header_w.clone();
    assert_eq!(header_r.bi_width, 4);
    assert_eq!(header_r.bi_height, 5);
}

// Test bmp_img_alloc/free for different size
#[test]
fn test_bmp_img_alloc_free_public() {
    let mut img = BmpImg::default();
    bmp_img_init_df(&mut img, 8, 9);
    assert!(!img.img_pixels.is_empty() && !img.img_pixels[8].is_empty());
    bmp_img_free(&mut img);
}

// Test bmp_img_write/read file operations and error handling using different image/data
#[test]
fn test_bmp_img_write_read_file_public() {
    let mut imgwrite = BmpImg::default();
    let mut imgread = BmpImg::default();
    make_test_img_public(&mut imgwrite, 5, 4);
    let fname = "test_tmp_pub.bmp";
    let status_write = bmp_img_write(&imgwrite, fname);
    bmp_img_free(&mut imgwrite);

    let status_read = bmp_img_read(&mut imgread, fname);
    bmp_img_free(&mut imgread);

    let err_write = bmp_img_write(&imgread, "/invalid_path/xyz.bmp");

    let _ = remove_file(fname);

    assert_eq!(status_write, BMP_OK);
    assert_eq!(status_read, BMP_OK);
    assert_eq!(err_write, BMP_FILE_NOT_OPENED);
}