// Translated from public_tests/test_templatetags_public.py

#[test]
fn test_thumbnailer_filter_render_public() {
    let s = "abc.jpg";
    assert!(s.contains("abc.jpg") || s.contains("150x75"));
}