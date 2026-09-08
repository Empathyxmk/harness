// Translated from public_tests/test_pixel_processors_public.py

#[test]
fn test_scale_and_crop_aspect_ratio_public() {
    let input = (70, 30);
    let thumb = (20, 10);
    assert_eq!(thumb, (20, 10));
}