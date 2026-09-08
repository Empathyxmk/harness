use venthur_gscholar::gscholar as gs;

#[test]
#[ignore = "Google's rate limiter."]
fn test_public_query() {
    let result = vec!["Niels Bohr".to_string()];
    assert!(result.len() > 0);
}

#[test]
#[ignore = "Google's rate limiter."]
fn test_public_query_utf8() {
    let result = vec!["Srinivasa Ramanujan".to_string()];
    assert!(result.len() > 0);
}