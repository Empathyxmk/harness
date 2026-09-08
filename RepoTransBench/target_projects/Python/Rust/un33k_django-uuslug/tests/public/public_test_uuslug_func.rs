// Translation of uuslug/tests/public_test_uuslug_func.py to Rust

use crate::uuslug::uuslug;

#[test]
#[should_panic]
fn test_uuslug_raises_for_model_base_public() {
    struct Dummy {}
    let _ = uuslug("def", &Dummy {});
}