use scastillo_siesta::*;

#[test]
fn test_foo_not_supported_print() {
    foo_not_supported();
}

#[test]
fn test_api_init_and_attr() {
    let api = API::new("http://publicapi.org", None);
    let resource = api.getattr("users");
    assert!(!resource.uri.is_empty());
    let resources = api.resources.lock().unwrap();
    assert!(resources.get("/users").is_some());
    assert_eq!(resource.uri, "/users");
    assert_eq!(resource.api.base_url, api.base_url);
    assert_eq!(format!("{}", api), "<API http://publicapi.org>");
    assert!(format!("{}", resource).starts_with("<Resource /users"));
}