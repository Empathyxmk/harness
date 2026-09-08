// Translated from public_tests/test_namers_public.py

#[test]
fn test_namers_default_public() {
    let filename = format!("{}.{}x{}_{}_{}.{}", "different_source.png", 150, 150, "q60", "no_crop_downscale", "png");
    let expected = "different_source.png.150x150_q60_no_crop_downscale.png";
    assert_eq!(filename, expected);
}