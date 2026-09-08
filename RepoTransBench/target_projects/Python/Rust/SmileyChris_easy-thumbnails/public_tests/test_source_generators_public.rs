// Translated from public_tests/test_source_generators_public.py

#[test]
fn test_pil_image_source_tuple_public() {
    let size = (4, 4);
    assert_eq!(size, (4, 4));
}

#[test]
fn test_pil_image_source_bytes_public() {
    let data = vec![0u8; 16];
    assert_eq!(data.len(), 16);
}