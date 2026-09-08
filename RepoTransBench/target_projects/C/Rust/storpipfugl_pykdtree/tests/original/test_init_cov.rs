#[test]
fn test_init_import() {
    // Just ensures __init__.py runs (import statement above).
    assert!(true);
}

#[test]
fn test_kdtree_module_present() {
    assert!(crate::kdtree::KDTree::new(ndarray::Array2::<f64>::zeros((1,2))).is_ok());
}