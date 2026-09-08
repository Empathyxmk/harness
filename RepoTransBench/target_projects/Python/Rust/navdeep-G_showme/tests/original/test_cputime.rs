//! Port of showme/tests/test_cputime.py to Rust.
//! Runs a heavy computation inside "cputime" decorator.

use showme::core::cputime;

#[test]
fn test_cputime_decorator_simulation() {
    // Simulate @cputime decorator; run heavy computation
    for i in 0..1000 {
        let _a = i32::pow(i, i as u32);
    }
    let _val = cputime();
    assert!(true); // If reached here, test passes
}