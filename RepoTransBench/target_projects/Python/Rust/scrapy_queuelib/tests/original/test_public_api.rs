#[test]
fn test_version_and_all_symbols() {
    // Simulate API presence check
    use scrapy_queuelib::*;
    assert_eq!(VERSION, "0.1.0");
    assert_eq!(__VERSION__, "0.1.0");

    // __all__ equivalent (API available in module namespace)
    // In Rust this is tested by the presence of symbols in crate root
    // pqueue, rrqueue should exist as modules, tested in public API test.
}