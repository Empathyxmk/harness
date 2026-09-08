//! Port of public_tests/test_public_cputime.py to Rust

use showme::core;

#[test]
fn test_public_cputime_runs() {
    // We can't predict cputime, just ensure it runs and returns a float
    let value = core::cputime();
    assert!(value >= 0.0 && value < 100_000.0);
}