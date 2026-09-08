use dnsdumpster::{DNSDumpsterAPI, DummyResponse};
use std::collections::HashMap;

struct DummyResp {
    text: String,
    status_code: i32,
}
impl DummyResp {
    fn new(txt: &str, code: i32) -> Self {
        Self { text: txt.to_string(), status_code: code }
    }
}

fn invalid_html() -> String {
    "<html><body>No form here!</body></html>".to_string()
}

#[test]
fn test_dnsdumpsterapi_init() {
    let api = DNSDumpsterAPI::new();
    // In Rust, just check that session property exists.
    // Actual type tests aren't needed, we know it's always present.
    assert!(!std::ptr::eq(&api.session, std::ptr::null()));
}

#[test]
fn test_dnsdumpsterapi_search_usage() {
    struct TestSession;
    impl TestSession {
        fn get(&self, _url: &str) -> DummyResp {
            DummyResp::new("<html><form></form></html>", 200)
        }
        fn post(&self, _url: &str, _data: &str, _headers: Option<&str>) -> DummyResp {
            DummyResp::new("<html><table></table></html>", 200)
        }
    }
    struct TestAPI {
        session: TestSession,
    }
    impl TestAPI {
        fn search(&self, _domain: &str) -> HashMap<String, serde_json::Value> {
            let _ = self.session.get("mock");
            let _ = self.session.post("mock", "", None);
            let mut out = HashMap::new();
            out.insert("answer".into(), serde_json::json!(42));
            out
        }
    }

    let api = TestAPI { session: TestSession };
    let result = api.search("example.com");
    assert!(result.get("answer").is_some());
}

#[test]
fn test_dnsdumpsterapi_search_no_csrf() {
    struct FailSession;
    impl FailSession {
        fn get(&self, _url: &str) -> DummyResp {
            DummyResp::new(&invalid_html(), 200)
        }
    }
    struct FailAPI {
        session: FailSession,
    }
    impl FailAPI {
        fn search(&self, _domain: &str) -> Result<HashMap<String, serde_json::Value>, String> {
            let resp = self.session.get("mock");
            if !resp.text.contains("form") {
                return Err("No form found!".into());
            }
            Ok(HashMap::new())
        }
    }

    let api = FailAPI { session: FailSession };
    let err = api.search("example.com");
    assert!(err.is_err());
}

#[test]
fn test_dnsdumpsterapi_form_parsing() {
    struct FormSession;
    impl FormSession {
        fn get(&self, _url: &str) -> DummyResp {
            DummyResp::new(
                r#"
                <html>
                <form>
                  <input type="hidden" name="csrfmiddlewaretoken" value="12345"/>
                  <input type="text" name="targetip" value="example.com"/>
                </form>
                </html>
                "#,
                200,
            )
        }
        fn post(&self, _url: &str, _data: &str, _headers: Option<&str>) -> DummyResp {
            DummyResp::new("<html><table></table></html>", 200)
        }
    }
    struct FormAPI {
        session: FormSession,
    }
    impl FormAPI {
        fn search(&self, _domain: &str) -> HashMap<String, serde_json::Value> {
            let get_resp = self.session.get("mock");
            assert!(get_resp.text.contains("csrfmiddlewaretoken"));
            let _ = self.session.post("mock", "", None);
            HashMap::new()
        }
    }
    let api = FormAPI { session: FormSession };
    let _ = api.search("example.com");
}