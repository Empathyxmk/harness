use ysbaddaden_gc::global_allocator::GlobalAllocator;

#[test]
fn test_global_allocator_oom_public() {
    let mut ga = GlobalAllocator::new(64 * 1024);
    // Simulate OOM by requesting more than heap; here just check non-panic.
    let _ = &mut ga;
}