// Translation of uuslug/tests/test_uuslug_func.py to Rust

#[test]
#[should_panic]
fn test_uuslug_raises_for_model_base() {
    // Simulate exception when a non-instance object is passed
    crate::uuslug::uuslug("abc", &());
}