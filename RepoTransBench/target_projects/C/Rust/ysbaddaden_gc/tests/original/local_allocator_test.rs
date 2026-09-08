use ysbaddaden_gc::local_allocator::LocalAllocator;

#[test]
fn test_local_allocator_simple_alloc() {
    let _ = LocalAllocator::new();
}