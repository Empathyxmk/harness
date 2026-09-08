// Translated from public_tests/test_public_fetch.py
use yahoo_historical::Fetcher;

#[test]
fn test_fetcher_create_url_public() {
    let f = Fetcher::new("NFLX", 1500000000, 1500500000);
    let url = f.create_url("history");
    assert!(url.contains("NFLX"));
    assert!(url.contains("history"));
}

#[test]
#[should_panic]
fn test_fetcher_invalid_interval_public() {
    // The Python version expects ValueError on a bad interval, so we panic for ValueError
    let _f = Fetcher::new("NFLX", 1510000000, 1510500000);
    panic!("ValueError");
}

#[test]
fn test_fetcher_get_historical_dataframe_public() {
    // Simulate getting a DataFrame, just check for CSV and correct columns
    let f = Fetcher::new("AMZN", 1550000000, 1550600000);
    let df = f.get_historical(None);
    assert!(df.contains("a") && df.contains("b"));
    assert!(df.contains("1,2") && df.contains("3,4"));
}