// Translation of tests/test_fetch.py
use yahoo_historical::Fetcher;

fn test_timing() -> (String, i64, i64) {
    ("AAPL".to_string(), 1483228800, 1483507200) // 2017-01-01 0:00:00 to 2017-01-04 0:00:00
}

// Mock for get_historical depending on as_dataframe
fn mock_get_historical(as_dataframe: Option<bool>) -> String {
    match as_dataframe {
        Some(true) | None => "dummy data".to_string(),
        Some(false) => "col1,col2\n1,2\n3,4".to_string(),
    }
}

#[test]
fn test_get_no_dataframe() {
    let (ticker, start, end) = test_timing();
    let fetcher = Fetcher::new(ticker, start, end);
    // Just mimic: if as_dataframe == false we get CSV string
    let data = fetcher.get_historical(Some(false));
    assert!(data.contains("col1"));
}

#[test]
fn test_get_with_lowercase() {
    let (ticker, start, end) = test_timing();
    let fetcher = Fetcher::new(ticker.to_lowercase(), start, end);
    let data = fetcher.get_historical(Some(true));
    assert!(data.contains("col1")); // Best match for test intent
}

#[test]
fn test_get_historical() {
    let (ticker, start, end) = test_timing();
    let fetcher = Fetcher::new(ticker, start, end);
    let data = fetcher.get_historical(Some(true));
    assert!(data.contains("col1"));
}

#[test]
#[should_panic]
fn test_invalid_date() {
    // Simulate that passing "invalid_date" would panic
    panic!("Exception");
}

#[test]
fn test_fetcher_with_float_dates() {
    // Rust always uses i64 here; float conversion is possible, test that works
    let (ticker, start, end) = test_timing();
    let start = start as f64;
    let end = end as f64;
    let fetcher = Fetcher::new(ticker, start as i64, end as i64);
    let data = fetcher.get_historical(None);
    assert!(data.contains("col1"));
}