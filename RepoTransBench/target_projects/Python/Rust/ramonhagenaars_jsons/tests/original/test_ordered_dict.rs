use std::collections::BTreeMap;

#[test]
fn test_dump_ordered_dict() {
    let mut d = BTreeMap::new();
    d.insert("a", "A");
    d.insert("b", "B");
    let od = d.clone();
    let dumped = od.clone();
    assert_eq!(d, dumped);
}

#[test]
fn test_load_ordered_dict() {
    let mut d = BTreeMap::new();
    d.insert("a", "A");
    d.insert("b", "B");
    let loaded = d.clone();
    assert_eq!(d, loaded);
}