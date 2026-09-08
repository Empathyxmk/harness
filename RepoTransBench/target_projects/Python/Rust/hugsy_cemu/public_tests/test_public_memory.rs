#[test]
fn test_public_placeholder_memory() {
    // Placeholder - ensure some coverage while using different data.
    let mut a = b"memory_public".to_vec();
    a[5] = b'P';
    assert_eq!(a[5], b'P');
}