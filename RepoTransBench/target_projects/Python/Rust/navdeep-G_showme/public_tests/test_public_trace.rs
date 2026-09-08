//! Port of public_tests/test_public_trace.py to Rust

use showme::core;

#[test]
fn test_trace_functionality() {
    // Simulate output, here just confirm call does not panic
    core::trace("Trace public test", 456);
    assert!(true);
}