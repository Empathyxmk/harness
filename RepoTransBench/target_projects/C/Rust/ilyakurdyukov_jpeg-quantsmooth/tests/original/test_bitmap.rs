use jpeg_quantsmooth::bitmap::Bitmap;

#[test]
fn test_bitmap_create_basic() {
    let bmp = Bitmap::create(10, 8, 3).unwrap(); // Basic valid input
    assert_eq!(bmp.width, 10);
    assert_eq!(bmp.height, 8);
    assert_eq!(bmp.bpp, 3);
    assert!(!bmp.data.is_empty());
}

#[test]
fn test_bitmap_create_overflow() {
    let bmp = Bitmap::create(100000, 10, 3);
    assert!(bmp.is_none());

    let bmp = Bitmap::create(10, 100000, 3);
    assert!(bmp.is_none());

    let bmp = Bitmap::create(-1, 10, 3);
    assert!(bmp.is_none());

    let bmp = Bitmap::create(10, -1, 3);
    assert!(bmp.is_none());

    let bmp = Bitmap::create(10, 10, -5);
    assert!(bmp.is_none());
}

#[test]
fn test_bitmap_create_minimal() {
    let bmp = Bitmap::create(1, 1, 1);
    assert!(bmp.is_some());
}

#[test]
fn test_bitmap_free_null() {
    Bitmap::free(None);
}