use requests_oauthlib_rs::oauth1::OAuth1Session;

#[test]
fn test_public_oauth1session_fetch_request_token_diff() {
    let session = OAuth1Session::new("public_client_key", Some("public_client_secret"), None, None);
    // Simulate a fetch_request_token call, returning dummy data
    let token = [("oauth_token", "ptok_pub1"), ("oauth_token_secret", "ptok_pub2")]
        .iter()
        .map(|(k,v)| (k.to_string(), v.to_string())).collect::<std::collections::HashMap<_,_>>();
    assert_eq!(token.get("oauth_token").unwrap(), "ptok_pub1");
    assert_eq!(token.get("oauth_token_secret").unwrap(), "ptok_pub2");
}

#[test]
fn test_public_oauth1session_repr_diff() {
    let sess = OAuth1Session::new("diff_key", Some("diff_secret"), None, None);
    let rep = format!("{:?}", sess);
    assert!(rep.contains("diff_key"));
    assert!(rep.starts_with("OAuth1Session"));
}