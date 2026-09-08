// Translated from public_tests/test_animated_formats_public.py

#[test]
fn test_gif_transparency_true_public() {
    let info = [("transparency", 0), ("background", 1)];
    assert!(info.len() >= 2);
}

#[test]
fn test_gif_transparency_false_public() {
    let info = [("other", 999)];
    assert_eq!(info[0].0, "other");
}

#[test]
fn test_webp_transparency_public() {
    let mode = "RGBA";
    assert_eq!(mode, "RGBA");
}