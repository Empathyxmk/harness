use crate::auth::{BasicAuth, TokenAuth};

struct DummyConfig {
    auth: Option<BasicAuth>,
}

#[test]
fn test_basic_auth_public() {
    let a = BasicAuth::new("user2", "pass2");
    assert_eq!(a.username, "user2");
    assert_eq!(a.password, "pass2");
}

#[test]
fn test_token_auth_public() {
    let t = TokenAuth::new("publictoken");
    assert_eq!(t.token, "publictoken");
}

#[test]
fn test_apply_auth_public() {
    let a = BasicAuth::new("alice", "secret123");
    let mut config = DummyConfig { auth: None };
    config.auth = Some(BasicAuth::new("alice", "secret123"));
    assert_eq!(config.auth.as_ref().unwrap().username, "alice");
    assert_eq!(config.auth.as_ref().unwrap().password, "secret123");
}