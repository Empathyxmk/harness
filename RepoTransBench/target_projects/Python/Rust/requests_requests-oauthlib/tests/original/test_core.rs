use std::collections::HashMap;

#[test]
fn test_set_token_public_diff_token() {
    use requests_oauthlib_rs::core::{set_token, TokenAssignable};
    struct DummySession {
        token: Option<HashMap<String, String>>,
    }
    impl TokenAssignable for DummySession {
        fn set_token(&mut self, t: HashMap<String, String>) {
            self.token = Some(t);
        }
        fn get_token(&self) -> Option<&HashMap<String, String>> {
            self.token.as_ref()
        }
    }
    let mut sess = DummySession { token: None };
    let mut tok = HashMap::new();
    tok.insert("access_token".to_string(), "unicorn_xyz".to_string());
    tok.insert("token_type".to_string(), "Bearer".to_string());
    set_token(&mut sess, tok);
    assert!(sess.token.is_some());
    let access_token = sess.token.as_ref().unwrap();
    assert!(access_token.contains_key("access_token"));
    assert_eq!(access_token.get("access_token").unwrap(), "unicorn_xyz");
}

#[test]
fn test_set_token_public_other_diff() {
    use requests_oauthlib_rs::core::{set_token, TokenAssignable};
    struct DummySession {
        token: Option<HashMap<String, String>>,
    }
    impl TokenAssignable for DummySession {
        fn set_token(&mut self, t: HashMap<String, String>) {
            self.token = Some(t);
        }
        fn get_token(&self) -> Option<&HashMap<String, String>> {
            self.token.as_ref()
        }
    }
    let mut sess = DummySession { token: None };
    let mut tok = HashMap::new();
    tok.insert("access_token".to_string(), "golden_public_token".to_string());
    tok.insert("token_type".to_string(), "macaroons".to_string());
    set_token(&mut sess, tok);
    assert!(sess.token.is_some());
    assert_eq!(sess.token.as_ref().unwrap().get("access_token").unwrap(), "golden_public_token");
}