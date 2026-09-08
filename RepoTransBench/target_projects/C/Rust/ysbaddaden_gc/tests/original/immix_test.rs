// Skeleton, you must fill details for full logic
#[test]
fn test_gc_malloc_small() {
    // Dummy allocation: In a real port, implement GC_malloc!
    let small = vec![0u8; 64];
    assert!(!small.is_empty());
}