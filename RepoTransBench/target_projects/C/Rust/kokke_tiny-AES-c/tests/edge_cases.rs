//! Edge case tests from kokke_tiny-AES-c/test_edge_cases.c (translated to Rust).
//! These test CBC, CTR, ECB behaviors for edge-case inputs.

use tiny_aes::*;
use std::cmp::min;

fn print_test(name: &str, condition: bool) {
    println!("{}: {}", name, if condition { "PASS" } else { "FAIL" });
    assert!(condition, "{}", name);
}

// The actual tests are implemented in ../original.rs because test_edge_cases.c logic
// is merged into one for Rust idiomatic test discovery.