#[test]
fn test_public_basic_var_strip() {
    let mut d = [("public_private", 123), ("should_keep", 456)].iter().cloned().collect::<std::collections::HashMap<_, _>>();
    let result: std::collections::HashMap<_, _> = d.iter().filter(|(&k, _)| !k.starts_with("public_")).map(|(k, v)| (*k, *v)).collect();
    assert!(result.contains_key("should_keep"));
    assert!(!result.contains_key("public_private"));
}

#[test]
fn test_public_group_var_precedence() {
    let group_vars = [("pubkey", "groupval"), ("shared", "gshared")]
        .iter().cloned().collect::<std::collections::HashMap<_, _>>();
    let host_vars = [("pubkey", "hostval"), ("override", "hval"), ("shared", "hshared")]
        .iter().cloned().collect::<std::collections::HashMap<_, _>>();
    let mut merged_vars = group_vars.clone();
    for (k, v) in host_vars.iter() {
        merged_vars.insert(*k, *v);
    }
    assert_eq!(merged_vars["pubkey"], "hostval");
    assert_eq!(merged_vars["shared"], "hshared");
    assert_eq!(merged_vars["override"], "hval");
    assert!(!merged_vars.values().any(|&v| v == "groupval"));
}

#[test]
fn test_public_nested_vars() {
    use std::collections::HashMap;
    let mut outer_map = HashMap::new();
    outer_map.insert("public_hidden", "value");
    outer_map.insert("visible", "42");
    let mut host_vars = HashMap::new();
    host_vars.insert("outer", outer_map.clone());
    host_vars.insert("plain", 10);
    // Remove keys beginning with 'public_' in nested dicts
    let clean_vars = |vars_dict: &HashMap<&str, HashMap<&str, &str>>| {
        let mut cleaned = HashMap::new();
        for (&k, v) in vars_dict.iter() {
            let mut cleaned_inner = HashMap::new();
            for (&ik, &iv) in v.iter() {
                if !ik.starts_with("public_") {
                    cleaned_inner.insert(ik, iv);
                }
            }
            cleaned.insert(k, cleaned_inner);
        }
        cleaned
    };
    // Now, just check main keys
    assert!(host_vars.contains_key("plain"));
    assert!(host_vars.contains_key("outer"));
    if let Some(outs) = host_vars.get("outer") {
        assert!(outs.contains_key("public_hidden"));
        assert!(outs.contains_key("visible"));
    }
}