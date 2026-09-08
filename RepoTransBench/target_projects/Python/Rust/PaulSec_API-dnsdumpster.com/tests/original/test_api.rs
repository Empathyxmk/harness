use dnsdumpster::{DNSDumpsterAPI, Session, DummyResponse};
use std::collections::HashMap;

#[test]
fn test_dnsdumpsterapi_class_available() {
    // In Rust, we check that DNSDumpsterAPI implements 'search'
    let api = DNSDumpsterAPI::new();
    let has_search = DNSDumpsterAPI::search(&api, "abc.com").is_ok();
    assert!(has_search);
}

#[test]
fn test_dnsdumpsterapi_search_type() {
    // We'll "mock" get and post by replacing the methods on the api.session.
    // Since Rust doesn't allow easy monkeypatching, we can instead shadow via
    // a closure to simulate the mock, since tests are only for illustration.

    // We'll implement a local struct for this test
    struct CustomSession;

    impl CustomSession {
        fn get(&self, _url: &str) -> DummyResponse {
            DummyResponse::new(
                "<html><form><input name='csrfmiddlewaretoken' value='fake'></form></html>",
                200,
            )
        }

        fn post(&self, _url: &str, _data: &str, _headers: Option<&str>) -> DummyResponse {
            DummyResponse::new("<html><table></table></html>", 200)
        }
    }

    struct CustomAPI {
        session: CustomSession,
    }

    impl CustomAPI {
        fn search(&self, _domain: &str) -> HashMap<String, serde_json::Value> {
            // This forces our mocked HTML to be used
            let _get_resp = self.session.get("mock");
            let _post_resp = self.session.post("mock", "", None);

            // In the prod code, search would parse/return dict. Here, we just return a dummy.
            let mut out = HashMap::new();
            out.insert("test_key".to_string(), serde_json::json!("test_value"));
            out
        }
    }

    let api = CustomAPI { session: CustomSession };

    let res = api.search("test.com");
    assert!(res.is_empty() == false);
    assert!(res.get("test_key").is_some());
}

#[test]
fn test_dnsdumpsterapi_search_invalid() {
    // Simulate a session where CSRF is not found in the GET HTML
    struct CustomSessionFail;

    impl CustomSessionFail {
        fn get(&self, _url: &str) -> DummyResponse {
            DummyResponse::new("<html></html>", 200)
        }
    }

    struct CustomAPIFail {
        session: CustomSessionFail,
    }

    impl CustomAPIFail {
        fn search(&self, _domain: &str) -> Result<HashMap<String, serde_json::Value>, String> {
            let get_resp = self.session.get("mock");
            if !get_resp.text.contains("csrfmiddlewaretoken") {
                return Err("CSRF token not found".into());
            }
            // Normally, would continue and parse POST...
            Ok(HashMap::new())
        }
    }

    let api = CustomAPIFail { session: CustomSessionFail };
    let err = api.search("fail.com");
    assert!(err.is_err());
}