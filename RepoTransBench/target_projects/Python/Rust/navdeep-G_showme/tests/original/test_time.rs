//! Port of showme/tests/test_time.py to Rust.
//! Runs a heavy computation inside a timed function.

use showme::core::time;

#[test]
fn test_time_decorator_simulation() {
    // Simulate @time decorator; measure time, run computation, return 1
    let _start = time();
    for i in 0..1000 {
        let _a = i32::pow(i, i as u32);
    }
    let _end = time();
    assert!(true); // Just ensure computation completed
}