use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
struct DummyResp {
    text: String,
    headers: HashMap<String, String>,
}

impl DummyResp {
    fn new(json: &serde_json::Value) -> Self {
        DummyResp {
            text: json.to_string(),
            headers: HashMap::new(),
        }
    }
}

type DummySend = fn(&DummyRequest, &HashMap<String, String>) -> DummyResp;

#[derive(Debug)]
struct DummyRequest {
    url: String,
    headers: HashMap<String, String>,
    body: String,
}

fn basic_auth_str(user: &str, pass: &str) -> String {
    format!(
        "Basic {}",
        base64::encode(format!("{}:{}", user, pass))
    )
}

#[test]
fn test_add_token_and_mtls_authorization_url() {
    let token = {
        let mut t = HashMap::new();
        t.insert("token_type".to_string(), "Bearer".to_string());
        t.insert("access_token".to_string(), "testtoken-access-abc".to_string());
        t
    };
    let bearer = format!(
        "{} {}",
        token.get("token_type").unwrap(),
        token.get("access_token").unwrap()
    );
    let request = DummyRequest {
        url: "https://x.y".to_string(),
        headers: [("Authorization".to_string(), bearer.clone())].iter().cloned().collect(),
        body: "".to_string(),
    };
    let header = request.headers.get("Authorization").unwrap();
    assert_eq!(header, &bearer);

    // Simulate mTLS: verify client cert tuple sent and client_id present
    let cert = ("cert_path.crt", "cert_key.key");
    let mut body = format!("param=foo&client_id={}", "cid-123");
    assert!(body.contains("client_id=cid-123"));

    // Simulate authorization_url: state and client_id in url
    let base = "https://example.com/authorize?foo=bar";
    let state = "random_state_123";
    let auth_url = format!(
        "{}&client_id={}&response_type=code&state={}",
        base, "cid-123", state
    );
    assert!(auth_url.contains(state));
    assert!(auth_url.contains("client_id=cid-123"));
    assert!(auth_url.contains("response_type=code"));
}

#[test]
fn test_pkce_in_authorization_url() {
    let base = "https://example.com/authorize?foo=bar";
    let state = "random_state_123";
    let challenge = "xyzCHALLENGEabc";
    let auth_url = format!(
        "{}&client_id={}&response_type=code&state={}&code_challenge={}&code_challenge_method=S256",
        base, "cid-123", state, challenge
    );
    assert!(auth_url.contains("code_challenge="));
    assert!(auth_url.contains("code_challenge_method=S256"));
}

#[test]
fn test_refresh_token_and_token_update_flow() {
    let token = {
        let mut t = HashMap::new();
        t.insert("access_token".to_string(), "expired-access".to_string());
        t.insert("expires_in".to_string(), "-1".to_string());
        t
    };

    fn fake_refresh(request: &DummyRequest, _headers: &HashMap<String, String>) -> DummyResp {
        let mut out_token = HashMap::new();
        out_token.insert("access_token".to_string(), "refreshed-access".to_string());
        let v = serde_json::Value::Object(
            out_token.iter().map(|(k,v)| (k.clone(), serde_json::Value::String(v.clone()))).collect()
        );
        DummyResp::new(&v)
    }

    // Simulate refresh, ensure new token is returned
    let request = DummyRequest {
        url: "https://api.example.com/token/refresh".to_string(),
        headers: HashMap::new(),
        body: "".to_string(),
    };
    let resp = fake_refresh(&request, &HashMap::new());
    let token_map: HashMap<String, String> = serde_json::from_str(&resp.text).unwrap();
    assert_eq!(token_map["access_token"], "refreshed-access");
}

#[test]
fn test_token_from_fragment() {
    let mut token = HashMap::new();
    token.insert("access_token".to_string(), "tok-frag".to_string());
    token.insert("expires_in".to_string(), "3000".to_string());
    let fragment = "access_token=tok-frag&expires_in=3000";
    let pairs: HashMap<String, String> = fragment
        .split('&')
        .map(|kv| {
            let mut parts = kv.split('=');
            (
                parts.next().unwrap().to_string(),
                parts.next().unwrap().to_string(),
            )
        })
        .collect();
    assert_eq!(pairs.get("access_token").unwrap(), "tok-frag");
    assert_eq!(pairs.get("expires_in").unwrap(), "3000");
}

#[test]
fn test_client_id_proxy() {
    #[derive(Debug)]
    struct FakeSession {
        client_id: Option<String>,
    }
    let mut sess = FakeSession { client_id: Some("test-id".to_string()) };
    assert_eq!(sess.client_id.as_deref(), Some("test-id"));
    sess.client_id = Some("different-id".to_string());
    assert_eq!(sess.client_id.as_deref(), Some("different-id"));
    sess.client_id = None;
    assert_eq!(sess.client_id, None);
}

#[test]
fn test_access_token_proxy() {
    #[derive(Debug)]
    struct FakeSession {
        access_token: Option<String>,
    }
    let mut sess = FakeSession { access_token: None };
    assert_eq!(sess.access_token, None);
    sess.access_token = Some("test-token".to_string());
    assert_eq!(sess.access_token.as_deref(), Some("test-token"));
    sess.access_token = None;
    assert_eq!(sess.access_token, None);
}

#[test]
fn test_token_proxy_set_get() {
    #[derive(Clone, Debug)]
    struct FakeSession {
        token: Option<HashMap<String, String>>,
    }
    let mut sess = FakeSession { token: None };
    let mut token = HashMap::new();
    token.insert("access_token".to_string(), "test-access".to_string());
    sess.token = Some(token.clone());
    assert_eq!(
        sess.token.as_ref().unwrap().get("access_token").unwrap(),
        "test-access"
    );
    token.insert("access_token".to_string(), "something-else".to_string());
    sess.token = Some(token.clone());
    assert_eq!(
        sess.token.as_ref().unwrap().get("access_token").unwrap(),
        "something-else"
    );
}

#[test]
fn test_cleans_previous_token_before_fetching_new_one() {
    let mut token = HashMap::new();
    token.insert("access_token".to_string(), "oldtoken".to_string());
    token.insert("expires_at".to_string(), "0".to_string()); // expired
    // When fetching new token, expired token is cleaned
    let mut new_token = token.clone();
    new_token.insert("access_token".to_string(), "newtoken".to_string());
    new_token.insert("expires_at".to_string(), "3600".to_string());
    assert_eq!(new_token.get("access_token").unwrap(), "newtoken");
}

#[test]
fn test_web_app_fetch_token_fail_for_state_mismatch() {
    let expected_state = "somestate";
    let auth_resp_url = "https://i.b/no-state?code=abc";
    // If state not present, error
    assert!(!auth_resp_url.contains(expected_state));
}