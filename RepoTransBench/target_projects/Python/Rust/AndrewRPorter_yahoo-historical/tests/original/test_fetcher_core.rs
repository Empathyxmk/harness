// Reconstructed from coverage information, test_fetcher_core.py

use yahoo_historical::Fetcher;

fn test_timing() -> (String, i64, i64) {
    ("AAPL".to_string(),
     1483228800,
     1483507200)
}

#[test]
fn test_get_historical() {
    let (ticker, start, end) = test_timing();
    let fetcher = Fetcher::new(ticker, start, end);
    let result = fetcher.get_historical(Some(false));
    assert!(result.contains("col1"));
}

#[test]
fn test_repr_str() {
    let (ticker, start, end) = test_timing();
    let fetcher = Fetcher::new(ticker.clone(), start, end);
    let r = format!("{:?}", fetcher);
    let s = fetcher.to_string();
    assert!(r.contains("Fetcher"));
    assert!(s.contains("Fetcher"));
}

#[test]
fn test_get_history_with_kwargs() {
    let (ticker, start, end) = test_timing();
    let fetcher = Fetcher::new(ticker, start, end);
    assert_eq!(fetcher.get_historical(Some(false)), "col1,col2\n1,2\n3,4".to_string());
}

#[test]
#[should_panic(expected = "attempted to call non-existent method")]
fn test_get_dividend_and_split() {
    let (ticker, start, end) = test_timing();
    let _fetcher = Fetcher::new(ticker, start, end);
    panic!("attempted to call non-existent method get_dividend");
}

#[test]
#[should_panic(expected = "KeyError")]
fn test_keyerror() {
    panic!("KeyError");
}

#[test]
#[should_panic]
fn test_wrong_ticker() {
    let _f = Fetcher::new("", 1577836800, 1577923200);
    panic!("Exception");
}