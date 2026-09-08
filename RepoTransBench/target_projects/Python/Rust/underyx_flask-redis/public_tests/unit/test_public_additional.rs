#[test]
fn test_truth_public() {
    // Slightly different, but checks True value
    assert!("nonempty".len() > 0, "Expected a non-empty string to evaluate as true");
}

#[test]
fn test_split_string_public() {
    let s = "foo bar baz";
    let parts: Vec<&str> = s.split_whitespace().collect();
    assert_eq!(parts, ["foo", "bar", "baz"]);
}

#[test]
fn test_sorted_list_public() {
    let mut lst = vec![10, 2, 4, 8];
    lst.sort();
    assert_eq!(lst, vec![2, 4, 8, 10]);
}

#[test]
fn test_dict_access_public() {
    use std::collections::HashMap;
    let mut d = HashMap::new();
    d.insert("alpha", 1);
    d.insert("beta", 2);
    assert_eq!(d["beta"], 2);
    assert!(d.contains_key("alpha"));
}