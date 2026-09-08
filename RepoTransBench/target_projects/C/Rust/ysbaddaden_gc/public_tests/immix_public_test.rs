use ysbaddaden_gc::immix::ImmixGc;

#[test]
fn test_gc_init_deinit_public() {
    let _gc = ImmixGc::new();
    // If doesn't panic, we pass.
}