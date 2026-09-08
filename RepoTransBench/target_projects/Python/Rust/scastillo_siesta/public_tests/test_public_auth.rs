use scastillo_siesta::*;

struct DummyRequestPublic {
    headers: std::collections::HashMap<String, String>,
}
impl DummyRequestPublic {
    fn new() -> Self {
        DummyRequestPublic {
            headers: std::collections::HashMap::new()
        }
    }
}

#[test]
fn test_basic_auth() {
    let a = auth::BasicAuth::new("alice", "wonderland");
    let hdrs = a.generate_headers();
    assert!(hdrs.get("Authorization").unwrap().starts_with("Basic "));
}

#[test]
fn test_call_sets_headers() {
    let a = auth::BasicAuth::new("alice", "wonderland");
    let mut req = TestRequest::new();
    a.attach(&mut req);
    assert!(req.headers.get("Authorization").is_some());
}

#[test]
fn test_repr() {
    let ba = auth::BasicAuth::new("someone", "secret");
    let rep = format!("{:?}", ba);
    assert!(rep.contains("BasicAuth"));
}

#[test]
fn test_bearer_token() {
    let bt = auth::BearerToken::new("publictoken456");
    let hdrs = bt.generate_headers();
    assert_eq!(hdrs.get("Authorization").unwrap(), "Bearer publictoken456");
    let mut req = TestRequest::new();
    bt.attach(&mut req);
    assert!(req.headers.get("Authorization").is_some());
}

#[test]
fn test_repr_bearer() {
    let b = auth::BearerToken::new("pubtoken");
    assert!(format!("{:?}", b).contains("BearerToken"));
}

#[test]
fn test_api_key_header_only() {
    let ak = auth::ApiKey::new("pubkey", "pubval", true);
    let hdrs = ak.generate_headers();
    assert!(hdrs.get("pubkey").is_some());
    let mut req = TestRequest::new();
    ak.attach(&mut req);
    assert!(req.headers.get("pubkey").is_some());
}

#[test]
fn test_api_key_in_query_not_supported() {
    let ak = auth::ApiKey::new("querykey", "queryval", false);
    let hdrs = ak.generate_headers();
    assert!(hdrs.is_empty());
}

#[test]
fn test_repr_api_key() {
    let ak = auth::ApiKey::new("pubapi", "pubvalue", true);
    assert!(format!("{:?}", ak).contains("ApiKey"));
}