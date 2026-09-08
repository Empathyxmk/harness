use std::collections::{HashMap, HashSet};
use spotify_pythonflow_rs::util;

#[test]
fn test_merge_dicts_actual() {
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
fn test_merge_dicts_conflict() {
    let mut a = HashMap::new();
    a.insert("z", 1);
    let mut b = HashMap::new();
    b.insert("z", 4);

    let m = util::merge_dicts(&a, &b);
    assert!(m.is_err());
}

#[test]
fn test_find_duplicates() {
    let items = vec![1, 2, 3, 2, 1, 5, 5];
    let dups = util::find_duplicates(&items);
    let hs: HashSet<i32> = [1, 2, 5].iter().copied().collect();
    assert_eq!(dups, hs);
}