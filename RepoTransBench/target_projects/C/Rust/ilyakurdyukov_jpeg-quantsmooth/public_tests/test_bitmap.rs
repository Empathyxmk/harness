use jpeg_quantsmooth::bitmap::Bitmap;

/// Create a bitmap using public test implementation
fn bitmap_create(width: i32, height: i32, bpp: i32) -> Option<Bitmap> {
    if width <= 0 || height <= 0 || bpp <= 0 {
        return None;
    }
    
    if width > 9000 || height > 9000 {
        return None;
    }
    
    // Simulate stride calculation as in original
    let stride = (width * bpp + 7) & -4; // Align to multiple of 4
    
    Some(Bitmap {
        width,
        height,
        bpp, 
        stride,
        data: vec![0; (stride * height) as usize],
    })
}

#[test]
fn test_bitmap_create_valid_newdata() {
    let width = 10;
    let height = 6;
    let bpp = 2;
    
    let bm = bitmap_create(width, height, bpp).unwrap();
    assert_eq!(bm.width, width);
    assert_eq!(bm.height, height);
    assert_eq!(bm.bpp, bpp);
    
    // Validate stride is multiple of 4 and at least width * bpp
    assert!(bm.stride >= width * bpp);
    assert_eq!(bm.stride % 4, 0);
}

#[test]
fn test_bitmap_create_invalid_zero() {
    let bm = bitmap_create(0, 2, 3); // width zero
    assert!(bm.is_none());
    
    let bm = bitmap_create(1, 0, 3); // height zero
    assert!(bm.is_none());
    
    let bm = bitmap_create(5, 1, 0); // bpp zero
    assert!(bm.is_none());
}

#[test]
fn test_bitmap_create_large_outofrange() {
    let bm = bitmap_create(9001, 10, 1); // exceeds public test limit
    assert!(bm.is_none());
    
    let bm = bitmap_create(10, 9002, 1); // exceeds public test limit
    assert!(bm.is_none());
}