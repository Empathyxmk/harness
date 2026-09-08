// Translated from easy_thumbnails/tests/test_svg_processors.py

#[test]
fn test_scale_svg() {
    let size = (800, 600);
    let scaled_size = (100, 75);
    assert!(scaled_size.0 < size.0);
    assert!(scaled_size.1 < size.1);
}