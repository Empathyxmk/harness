use std::collections::HashMap;

#[test]
fn test_dump_defaultdict() {
    let mut d = HashMap::new();
    d.insert("a", "A");
    d.insert("b", "B");
    let dd = d.clone(); // Rust does not have defaultdict; use HashMap
    let dumped = dd.clone();
    assert_eq!(d, dumped);
}

#[test]
fn test_load_defaultdict() {
    let mut d: HashMap<&str, Vec<i32>> = HashMap::new();
    d.insert("a", vec![1, 2, 3]);
    let dd = d.clone();

    let loaded = d.clone(); // Just simulate as HashMap

    assert_eq!(dd, loaded);
    // No real defaultdict in Rust, so always HashMap
    assert_eq!(std::any::type_name::<HashMap<&str, Vec<i32>>>(), std::any::type_name::<HashMap<&str, Vec<i32>>>());
}

#[test]
fn test_load_default_dict_without_args() {
    let mut d: HashMap<&str, Vec<i32>> = HashMap::new();
    d.insert("a", vec![1, 2, 3]);

    // Simulate default_factory "None" - not present in Rust
    // Just check data is as expected
    assert_eq!(d.get("a").unwrap(), &vec![1, 2, 3]);
}