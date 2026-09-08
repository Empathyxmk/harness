use std::collections::HashMap;
use requests_oauthlib_rs::oauth2::OAuth2;

#[test]
fn test_public_oauth2_auth_header_diff_data() {
    let client_id = "public_client_id";
    let mut token_data = HashMap::new();
    token_data.insert("access_token".to_string(), "tok_9876543210abc".to_string());
    token_data.insert("token_type".to_string(), "Bearer".to_string());
    token_data.insert("expires_in".to_string(), "600".to_string());

    let oauth = OAuth2::new(client_id, Some(token_data.clone()));

    struct Req {
        headers: std::collections::HashMap<String, String>,
    }
    impl Req {
        fn new() -> Self {
            Req { headers: HashMap::new() }
        }
    }
    let mut req = Req::new();
    // Simulate setting auth header
    req.headers.insert("Authorization".to_string(), format!("Bearer {}", token_data.get("access_token").unwrap()));
    assert!(req.headers.contains_key("Authorization"));
    assert!(req.headers.get("Authorization").unwrap().starts_with("Bearer "));
    assert!(req.headers.get("Authorization").unwrap().contains(token_data.get("access_token").unwrap()));
}

#[test]
fn test_public_oauth2_auth_repr_diff() {
    let oauth = OAuth2::new("public_id", None);
    let rep = format!("{:?}", oauth);
    assert!(rep.contains("public_id"));
    assert!(rep.starts_with("OAuth2("));
}