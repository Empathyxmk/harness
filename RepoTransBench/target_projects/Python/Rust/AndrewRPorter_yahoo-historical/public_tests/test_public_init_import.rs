// Translated from public_tests/test_public_init_import.py
use yahoo_historical::Fetcher;

#[test]
fn test_import_fetcher_public() {
    // Different ticker/dates from original for public variant
    let f = Fetcher::new("msft", 1650000000, 1650001000);
    let s = f.get_historical(None);
    assert!(s.contains("col1"));
}