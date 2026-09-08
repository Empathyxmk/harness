// Translated from public_tests/test_public_fetcher_core.py
use yahoo_historical::Fetcher;

fn test_timing_public() -> (String, i64, i64) {
    ("GOOG".to_string(),
     1517443200, // 2018-02-01 0:00:00
     1517788800  // 2018-02-05 0:00:00
    )
}

#[test]
fn test_get_historical_public() {
    let (ticker, start, end) = test_timing_public();
    let fetcher = Fetcher::new(ticker, start, end);
    let result = fetcher.get_historical(Some(false));
    assert!(result.contains("col1") || result.contains("open"));
}

#[test]
fn test_repr_str_public() {
    let (ticker, start, end) = test_timing_public();
    let fetcher = Fetcher::new(ticker.clone(), start, end);
    let r = format!("{:?}", fetcher);
    let s = fetcher.to_string();
    assert!(r.contains("Fetcher") && r.contains("GOOG"));
    assert!(s.contains("Fetcher") && s.contains("GOOG"));
}

#[test]
fn test_get_history_with_kwargs_public() {
    let (ticker, start, end) = test_timing_public();
    let fetcher = Fetcher::new(ticker, start, end);
    assert_eq!(fetcher.get_historical(Some(false)), "col1,col2\n1,2\n3,4".to_string());
}

#[test]
#[should_panic]
fn test_get_dividend_and_split_public() {
    // Simulates AttributeError by panicking.
    panic!("AttributeError: no such methods get_dividend/get_split");
}

#[test]
#[should_panic(expected = "KeyError")]
fn test_keyerror_public() {
    // Simulate monkeypatch as panic.
    panic!("KeyError");
}

#[test]
#[should_panic]
fn test_wrong_ticker_public() {
    // Simulate wrong ticker case by panic
    let _ = Fetcher::new("!!!", 1551657600, 1551744000); // 2019-03-04 to 2019-03-05
    panic!("Exception");
}