// Original: "advanced" test for hmm

use samplemod_rs::core;

#[test]
fn test_thoughts() {
    // sample.hmm() returns None in Python; in Rust, it prints.
    // Just check that calling hmm() does not panic and returns ().
    assert_eq!(core::hmm(), ());
}