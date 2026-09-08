use scastillo_siesta::*;

#[test]
fn test_foo_not_supported_print() {
    foo_not_supported();
}

#[test]
fn test_api_init_and_attr() {
    let api = API::new("http://api.com", None);
    let resource = api.getattr("books");
    assert!(resource.uri == "/books");
    let resources = api.resources.lock().unwrap();
    assert!(resources.get("/books").is_some());
    assert_eq!(resource.api.base_url, api.base_url);
    assert_eq!(format!("{}", api), "<API http://api.com>");
    assert!(format!("{}", resource).starts_with("<Resource /books"));
}