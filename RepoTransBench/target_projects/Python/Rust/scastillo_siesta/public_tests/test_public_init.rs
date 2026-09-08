use scastillo_siesta::*;
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Debug)]
struct DummyAPI {
    base_url: String,
    resources: HashMap<String, Arc<Resource>>,
}
impl DummyAPI {
    fn new() -> Self {
        DummyAPI {
            base_url: "http://anotherdomain.com".to_string(),
            resources: HashMap::new(),
        }
    }
}

#[test]
fn test_resource_init() {
    let api = Arc::new(DummyAPI::new());
    let mut headers = HashMap::new();
    headers.insert("User-Agent".to_string(), USER_AGENT.to_string());
    let res = Resource {
        uri: "/another_endpoint".to_string(),
        api: Arc::new(API::new("http://anotherdomain.com", None)),
        id: None,
        headers: headers.clone(),
    };
    assert_eq!(res.uri, "/another_endpoint");
    assert!(res.id.is_none());
    assert_eq!(res.headers["User-Agent"], USER_AGENT);
}

#[test]
fn test_getattr_new_resource() {
    let api = API::new("http://anotherdomain.com", None);
    let r = api.getattr("books");
    assert_eq!(r.uri, "/books");
    let resources = api.resources.lock().unwrap();
    assert!(resources.get("/books").is_some());
}

#[test]
fn test_call_with_id() {
    let api = API::new("http://anotherdomain.com", None);
    let r = api.getattr_call("books", 101);
    // Accepts r.id Some("101")
    assert_eq!(r.id, Some("101".to_string()));
    assert!(r.uri.ends_with("/books/101"));
}

#[test]
fn test_set_request_type_json() {
    let mut api = API::new("http://anotherdomain.com", None);
    let mut resource = Resource::new("/another_endpoint", Arc::new(api));
    resource.set_request_type("json");
    assert_eq!(resource.headers["Accept"], "application/json");
    resource.set_request_type("json"); // Idempotent
    assert_eq!(resource.headers["Accept"], "application/json");
}

#[test]
fn test_set_request_type_xml() {
    let mut api = API::new("http://anotherdomain.com", None);
    let mut resource = Resource::new("/another_endpoint", Arc::new(api));
    resource.set_request_type("xml");
    assert_eq!(resource.headers["Accept"], "application/xml");
    resource.set_request_type("xml"); // Idempotent
    assert_eq!(resource.headers["Accept"], "application/xml");
}

#[test]
fn test_get_simple() {
    let api = API::new("http://anotherdomain.com", None);
    let resource = Resource::new("/another_endpoint", Arc::new(api));
    let result = resource.get();
    assert_eq!(result.get("result"), Some(&"ok".to_string()));
}

#[test]
fn test_post_simple() {
    let api = API::new("http://anotherdomain.com", None);
    let resource = Resource::new("/another_endpoint", Arc::new(api));
    let result = resource.post(&[("hello", "world")]);
    assert_eq!(result.get("result"), Some(&"ok".to_string()));
}

#[test]
fn test_put_with_id() {
    let api = API::new("http://anotherdomain.com", None);
    let mut resource = Resource::new("/another_endpoint", Arc::new(api));
    resource.id = Some("99".to_string());
    let result = resource.put(&[("update", "yes")]);
    assert!(result.is_some());
}

#[test]
fn test_put_without_id() {
    let api = API::new("http://anotherdomain.com", None);
    let mut resource = Resource::new("/another_endpoint", Arc::new(api));
    resource.id = None;
    let result = resource.put(&[("update", "no")]);
    assert!(result.is_none());
}

#[test]
fn test_delete_with_id() {
    let api = API::new("http://anotherdomain.com", None);
    let mut resource = Resource::new("/another_endpoint", Arc::new(api));
    resource.id = Some("88".to_string());
    let result = resource.delete();
    assert!(result.is_some());
}

#[test]
fn test_delete_without_id() {
    let api = API::new("http://anotherdomain.com", None);
    let mut resource = Resource::new("/another_endpoint", Arc::new(api));
    resource.id = None;
    let result = resource.delete();
    assert!(result.is_none());
}

#[test]
fn test_repr() {
    let api = API::new("http://anotherdomain.com", None);
    let resource = Resource::new("/another_endpoint", Arc::new(api));
    let s = format!("{}", resource);
    assert!(s.contains("/another_endpoint"));
}

#[test]
fn test_api_init_repr() {
    let api = API::new("http://newuri", Some("y".to_string()));
    assert_eq!(api.base_url, "http://newuri");
    assert_eq!(api.auth, Some("y".to_string()));
    let s = format!("{:?}", api);
    assert!(s.contains("http://newuri"));
}

#[test]
fn test_api_getattr() {
    let api = API::new("http://newuri", None);
    let res = api.getattr("bar");
    assert_eq!(res.uri, "/bar");
    let resources = api.resources.lock().unwrap();
    assert!(resources.get("/bar").is_some());
}

#[test]
fn test_foo_not_supported() {
    foo_not_supported();
}