use std::collections::HashMap;
use spotify_pythonflow_rs::util;

#[test]
fn test_merge_dicts_public() {
    let mut a = HashMap::new();
    a.insert("e", 1);
    a.insert("f", 2);
    let mut b = HashMap::new();
    b.insert("g", 3);
    let m = util::merge_dicts(&a, &b).unwrap();
    assert_eq!(m["e"], 1);
    assert_eq!(m["f"], 2);
    assert_eq!(m["g"], 3);
}

#[test]
fn test_merge_dicts_conflict_public() {
    let mut a = HashMap::new();
    a.insert("z", 1);
    let mut b = HashMap::new();
    b.insert("z", 4);
    let m = util::merge_dicts(&a, &b);
    assert!(m.is_err());
}

#[test]
fn test_find_duplicates_public() {
    let items = vec![1, 2, 3, 2, 1, 5, 5];
    let dups = util::find_duplicates(&items);
    assert_eq!(dups, [1, 2, 5].iter().cloned().collect());
}