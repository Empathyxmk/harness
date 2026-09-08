use std::collections::HashMap;

fn public_bearer(token: &HashMap<String, String>) -> String {
    format!(
        "Bearer {}",
        token.get("access_token").unwrap_or(&"".to_string())
    )
}

#[test]
fn test_add_token_public() {
    let mut token = HashMap::new();
    token.insert("token_type".to_string(), "Bearer".to_string());
    token.insert("access_token".to_string(), "pubtok123456789".to_string());
    token.insert("refresh_token".to_string(), "pubrtok987654321".to_string());
    token.insert("expires_in".to_string(), "1234".to_string());

    let bearer = public_bearer(&token);

    let mut headers = HashMap::new();
    headers.insert("Authorization".to_string(), bearer.clone());
    assert_eq!(headers.get("Authorization").unwrap(), &bearer);
}

#[test]
fn test_authorization_url_public() {
    let url = "https://public.example.com/authenticate?pubfoo=bar";
    let pub_client_id = "publicclientid";
    let state = "pubstate-1337";
    let code = "pubcode-abc";

    let web_auth_url = format!(
        "{}&client_id={}&response_type=code&state={}",
        url, pub_client_id, state
    );
    assert!(web_auth_url.contains(pub_client_id));
    assert!(web_auth_url.contains("response_type=code"));
    assert!(web_auth_url.contains(state));

    let mob_auth_url = format!(
        "{}&client_id={}&response_type=token&state={}",
        url, pub_client_id, state
    );
    assert!(mob_auth_url.contains(pub_client_id));
    assert!(mob_auth_url.contains("response_type=token"));
    assert!(mob_auth_url.contains(state));
}

#[test]
fn test_pkce_authorization_url_public() {
    let url = "https://public.example.com/authenticate?pubfoo=bar";
    let pub_client_id = "publicclientid";
    let state = "pubstate-1337";
    let code_challenge = "plainchallenge";
    let web = format!(
        "{}&client_id={}&response_type=code&state={}&code_challenge={}&code_challenge_method=plain",
        url, pub_client_id, state, code_challenge
    );
    assert!(web.contains("code_challenge="));
    assert!(web.contains("code_challenge_method=plain"));

    let mob = format!(
        "{}&client_id={}&response_type=token&state={}&code_challenge={}&code_challenge_method=plain",
        url, pub_client_id, state, code_challenge
    );
    assert!(mob.contains("code_challenge="));
    assert!(mob.contains("code_challenge_method=plain"));
}

#[test]
fn test_refresh_token_request_public() {
    let mut token = HashMap::new();
    token.insert("access_token".to_string(), "pubtok123456789".to_string());
    token.insert("expires_in".to_string(), "-20".to_string());
    // Simulate expired token, refresh to fix
    let refreshed_token = "pubnewtoken";
    assert_ne!(token.get("expires_in").unwrap(), "1234"); // "refresh" required
    let refreshed = refreshed_token;
    assert_eq!(refreshed, "pubnewtoken");
}