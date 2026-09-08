use crate::auth::{BasicAuth, TokenAuth, FlaskForwardAuth};

#[test]
fn test_basic_auth() {
    let auth = BasicAuth::new("tester", "pword");
    assert_eq!(auth.username, "tester");
    assert_eq!(auth.password, "pword");
}

#[test]
fn test_token_auth() {
    let t = TokenAuth::new("tokentest");
    assert_eq!(t.token, "tokentest");
}

#[test]
fn test_flask_forward_auth_instance() {
    let _ff = FlaskForwardAuth::new();
}