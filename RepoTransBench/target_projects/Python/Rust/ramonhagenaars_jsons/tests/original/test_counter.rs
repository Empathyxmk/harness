use std::collections::HashMap;

#[test]
fn test_dump_counter() {
    let s = "A counter is something that counts!";
    let mut c = HashMap::new();
    for ch in s.chars() {
        *c.entry(ch).or_insert(0) += 1;
    }
    let expected = [
        ('A', 1), (' ', 5), ('c', 2), ('o', 3), ('u', 2), ('n', 3), ('t', 5),
        ('e', 2), ('r', 1), ('i', 2), ('s', 3), ('m', 1), ('h', 2), ('g', 1),
        ('a', 1), ('!', 1),
    ].iter().cloned().collect::<HashMap<char, i32>>();
    assert_eq!(c, expected);
}

#[test]
fn test_load_counter() {
    let d = [
        ('A', 1), (' ', 5), ('c', 2), ('o', 3), ('u', 2), ('n', 3), ('t', 5),
        ('e', 2), ('r', 1), ('i', 2), ('s', 3), ('m', 1), ('h', 2), ('g', 1),
        ('a', 1), ('!', 1),
    ].iter().cloned().collect::<HashMap<char, i32>>();
    let loaded = d.clone();
    // Count equality (order does not matter)
    assert_eq!(d, loaded);
}