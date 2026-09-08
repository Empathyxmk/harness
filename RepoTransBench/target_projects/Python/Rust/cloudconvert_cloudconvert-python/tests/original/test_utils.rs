use cloudconvert_cloudconvert_rust::utils;

#[test]
fn test_slugify() {
    let s = utils::slugify("Hello, world!");
    assert_eq!(s, "hello-world");
}

#[test]
fn test_generate_id() {
    let id1 = utils::generate_id();
    let id2 = utils::generate_id();
    assert_ne!(id1, id2);
}