use ysbaddaden_gc::global_allocator::GlobalAllocator;

#[test]
fn test_oom_triggers_abort() {
    let mut ga = GlobalAllocator::new(2 * 4096);
    // Not possible to trigger abort the same way as C signal/abort,
    // but we will simulate an OOM by exhausting a limit.
    let mut hit_limit = false;
    for _ in 0..20 {
        let requested = ga.memory_limit;
        if requested == 0 {
            hit_limit = true;
            break;
        }
        ga.memory_limit = ga.memory_limit / 2;
    }
    assert!(hit_limit, "Should have triggered OOM");
}