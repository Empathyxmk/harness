// Already present and previously implemented, unchanged.
use yahoo_historical::Fetcher;

#[test]
fn test_import_fetcher() {
    let _ = Fetcher::new("aapl", 1600000000, 1600001000);
    // There's no direct equivalent to hasattr in Rust, but we check method exists via trait/object.
    let f = Fetcher::new("aapl", 1600000000, 1600001000);
    // Confirm Fetcher type has get_historical by calling and checking the string result.
    let s = f.get_historical(None);
    assert!(s.contains("col1"));
}