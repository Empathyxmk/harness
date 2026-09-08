use ysbaddaden_gc::local_allocator::LocalAllocator;
use ysbaddaden_gc::global_allocator::GlobalAllocator;

#[test]
fn test_local_allocator_public() {
    let _global = GlobalAllocator::new(128*1024);
    let _local = LocalAllocator::new();
}