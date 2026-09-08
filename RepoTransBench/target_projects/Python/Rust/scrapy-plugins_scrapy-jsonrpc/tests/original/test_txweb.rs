use scrapy_jsonrpc::txweb::{JsonResource, DummyRequestTrait};
use serde_json::json;

struct DummyRequest {
    pub _headers: std::collections::HashMap<String, String>,
}
impl DummyRequest {
    fn new() -> Self {
        DummyRequest { _headers: std::collections::HashMap::new() }
    }
}
impl DummyRequestTrait for DummyRequest {
    fn set_header(&mut self, k: &str, v: &str) {
        self._headers.insert(k.to_string(), v.to_string());
    }
}

#[test]
fn test_jsonresource_render_object_sets_headers_and_returns_json() {
    let jr = JsonResource;
    let obj = json!({"foo": "bar"});
    let mut dr = DummyRequest::new();
    let res = jr.render_object(&obj, &mut dr);
    assert!(res.trim().starts_with("{") && res.trim().ends_with("}"));
    assert_eq!(dr._headers.get("Content-Type").unwrap(), "application/json");
    assert_eq!(dr._headers.get("Access-Control-Allow-Origin").unwrap(), "*");
    assert_eq!(dr._headers.get("Access-Control-Allow-Methods").unwrap(), "GET, POST, PATCH, PUT, DELETE");
    assert_eq!(dr._headers.get("Access-Control-Allow-Headers").unwrap(), " X-Requested-With");
    assert_eq!(dr._headers.get("Content-Length").unwrap().parse::<usize>().unwrap(), res.len());
}