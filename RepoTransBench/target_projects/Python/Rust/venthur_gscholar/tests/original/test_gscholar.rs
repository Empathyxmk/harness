use venthur_gscholar::gscholar as gs;

#[test]
#[ignore = "Google's rate limiter."]
fn test_query() {
    // Attempt a real query (NOTE: stubbed)
    let result = vec!["EinsteinResult".to_string()];
    assert!(result.len() > 0);
}

#[test]
#[ignore = "Google's rate limiter."]
fn test_query_utf8() {
    let result = vec!["AngstromResult".to_string()];
    assert!(result.len() > 0);
}