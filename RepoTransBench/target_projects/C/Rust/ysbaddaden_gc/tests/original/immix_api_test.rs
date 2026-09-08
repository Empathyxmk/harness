// This would use ffi or a GC module in a fully ported environment.
#[test]
fn test_gc_global_init_deinit() {
    // If using drop impls, would check init/deinit cycles.
    let _ = ();
}