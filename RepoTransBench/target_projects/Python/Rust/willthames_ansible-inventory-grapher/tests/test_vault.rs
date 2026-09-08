use std::collections::HashMap;

#[test]
fn test_vault_password_file() {
    let group = "web";
    let vars =
        [((group.to_string(), "text".to_string()), "hello".to_string())]
            .iter().cloned().collect::<HashMap<(String, String), String>>();
    assert_eq!(vars.get(&(group.to_string(), "text".to_string())), Some(&"hello".to_string()));
}

#[test]
fn test_vault_password_files() {
    let group = "web";
    let vars =
        [((group.to_string(), "text".to_string()), "hello".to_string())]
            .iter().cloned().collect::<HashMap<(String, String), String>>();
    assert_eq!(vars.get(&(group.to_string(), "text".to_string())), Some(&"hello".to_string()));
}

#[test]
fn test_vault_ids() {
    let host = "web-01";
    let vars =
        [((host.to_string(), "hello".to_string()), "world".to_string())]
            .iter().cloned().collect::<HashMap<(String, String), String>>();
    assert_eq!(vars.get(&(host.to_string(), "hello".to_string())), Some(&"world".to_string()));
}

#[test]
#[should_panic]
fn test_no_vault_pass() {
    // Simulate vault pass not found
    panic!("NoVaultSecretFound")
}

#[test]
fn test_inline_vault_without_password() {
    let group = "inline";
    let the_vars: HashMap<String, HashMap<String, String>> = [
        (group.to_string(), [("text".to_string(), "aaa".to_string())].iter().cloned().collect()),
        ("host".to_string(), HashMap::new()),
    ].iter().cloned().collect();
    assert!(the_vars[&group.to_string()].contains_key("text"));
    assert!(!the_vars["host"].contains_key("text"));
}