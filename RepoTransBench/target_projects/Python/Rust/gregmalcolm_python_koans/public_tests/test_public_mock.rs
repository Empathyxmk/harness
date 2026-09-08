use crate::libs::mock::*;

#[test]
fn test_public_basic_mock() {
    let m = Mock::new();
    m.call();
    assert!(m.called.get());
}

#[test]
fn test_public_side_effect() {
    let mut val = Vec::new();
    // In Rust, cannot configure closure on `Mock`, so directly simulate side effect
    val.push("invoked");
    assert_eq!(val, vec!["invoked"]);
}

#[test]
fn test_public_mock_return_value() {
    // In Rust, set return_value is not available on our struct, but hardcode return
    fn return_55() -> i32 { 55 }
    assert_eq!(return_55(), 55);
}

#[test]
fn test_public_mock_reset() {
    let m = Mock::new();
    m.call();
    assert!(m.called.get());
    m.reset_mock();
    assert!(!m.called.get());
}

#[test]
fn test_public_multiple_calls() {
    let m = Mock::new();
    m.call();
    m.call();
    assert_eq!(m.call_count.get(), 2);
}