use rbarrois_xworkflows::utils;

#[test]
fn test_iterclass_traversal_different() {
    struct C {}
    struct D {}
    let result = utils::iterclass(&D{});
    assert_eq!(result["x"], 10);
    assert_eq!(result["y"], 20);
}

#[test]
fn test_iterclass_overrides_different() {
    struct C {}
    struct D {}
    let result = utils::iterclass(&D{});
    assert_eq!(result["alpha"], 42);
}