use scastillo_siesta::*;

struct DummyRequest {
    headers: std::collections::HashMap<String, String>,
}
impl DummyRequest {
    fn new() -> Self {
        DummyRequest {
            headers: std::collections::HashMap::new()
        }
    }
}

#[test]
fn test_basic_auth() {
    let a = auth::BasicAuth::new("foo", "bar");
    let hdrs = a.generate_headers();
    assert!(hdrs.get("Authorization").unwrap().starts_with("Basic "));
}

#[test]
fn test_call_sets_headers() {
    let a = auth::BasicAuth::new("foo", "bar");
    let mut req = TestRequest::new();
    a.attach(&mut req);
    assert!(req.headers.get("Authorization").is_some());
}

#[test]
fn test_repr() {
    let ba = auth::BasicAuth::new("username", "pw");
    let rep = format!("{:?}", ba);
    assert!(rep.contains("BasicAuth"));
}

#[test]
fn test_bearer_token() {
    let bt = auth::BearerToken::new("tok123");
    let hdrs = bt.generate_headers();
    assert_eq!(hdrs.get("Authorization").unwrap(), "Bearer tok123");
    let mut req = TestRequest::new();
    bt.attach(&mut req);
    assert!(req.headers.get("Authorization").is_some());
}

#[test]
fn test_repr_bearer() {
    let b = auth::BearerToken::new("tk");
    assert!(format!("{:?}", b).contains("BearerToken"));
}

#[test]
fn test_api_key_header_only() {
    let ak = auth::ApiKey::new("mykey", "myval", true);
    let hdrs = ak.generate_headers();
    assert!(hdrs.get("mykey").is_some());
    let mut req = TestRequest::new();
    ak.attach(&mut req);
    assert!(req.headers.get("mykey").is_some());
}

#[test]
fn test_api_key_in_query_not_supported() {
    let ak = auth::ApiKey::new("qkey", "qval", false);
    let hdrs = ak.generate_headers();
    assert!(hdrs.is_empty()); // Prints msg in Python, but not here, but test expects {}.
}

#[test]
fn test_repr_api_key() {
    let ak = auth::ApiKey::new("api", "value", true);
    assert!(format!("{:?}", ak).contains("ApiKey"));
}