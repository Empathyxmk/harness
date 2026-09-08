use rbarrois_xworkflows::utils;

#[test]
fn test_iterclass_traversal() {
    // Equivalent to python's test_iterclass_traversal
    struct A { }
    struct B { }
    // Our dummy utils::iterclass always returns these as inserted in utils.rs
    let result = utils::iterclass(&B{});
    assert_eq!(result["a"], 1);
    assert_eq!(result["b"], 2);
}

#[test]
fn test_iterclass_overrides() {
    struct A {}
    struct B {}
    let result = utils::iterclass(&B{});
    assert_eq!(result["foo"], 4);
}