// Translated from public_tests/test_public_constants.py
use yahoo_historical::constants;

#[test]
fn test_constants_fields_public() {
    // Ensure API_URL, DATE_INTERVALS, ONE_DAY_INTERVAL are available
    assert!(!constants::API_URL.is_empty());
    assert_eq!(constants::ONE_DAY_INTERVAL, "1d");
    assert!(constants::DATE_INTERVALS.contains(&"1d"));
}

#[test]
fn test_api_url_format_public() {
    // Use example values (like TSLA, 1610000000, etc)
    let url = format!(
        constants::API_URL,
        "TSLA", "1610000000", "1610020000", "1d", "history"
    );
    assert!(url.contains("TSLA"));
    assert!(url.contains("16100"));
    assert!(url.contains("1d"));
    let history_pos = url.find("history");
    assert!(history_pos.is_some());
    assert!(history_pos.unwrap() > 0);
}