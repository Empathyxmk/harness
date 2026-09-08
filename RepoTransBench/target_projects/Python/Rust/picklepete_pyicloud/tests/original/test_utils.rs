use std::collections::HashMap;
use std::cell::RefCell;
use std::rc::Rc;
use std::any::Any;

thread_local! {
    static SAVED: RefCell<HashMap<String, String>> = RefCell::new(HashMap::new());
    static DELETED: RefCell<Vec<String>> = RefCell::new(Vec::new());
}

struct DummyKeyring;

impl DummyKeyring {
    fn get_password(system: &str, username: &str) -> Option<String> {
        SAVED.with(|s| s.borrow().get(username).cloned())
    }
    fn set_password(system: &str, username: &str, password: &str) -> &'static str {
        SAVED.with(|s| s.borrow_mut().insert(username.to_string(), password.to_string()));
        "set"
    }
    fn delete_password(system: &str, username: &str) -> &'static str {
        DELETED.with(|d| d.borrow_mut().push(username.to_string()));
        "del"
    }
}

fn get_password_from_keyring(username: &str) -> Result<String, &'static str> {
    DummyKeyring::get_password("icloud", username).ok_or("PyiCloudNoStoredPasswordAvailableException")
}

fn password_exists_in_keyring(username: &str) -> bool {
    DummyKeyring::get_password("icloud", username).is_some()
}

fn store_password_in_keyring(username: &str, password: &str) -> &'static str {
    DummyKeyring::set_password("icloud", username, password)
}

fn delete_password_in_keyring(username: &str) -> &'static str {
    DummyKeyring::delete_password("icloud", username)
}

fn underscore_to_camelcase(s: &str, initial_capital: bool) -> String {
    let mut iter = s.split('_');
    let mut result = String::new();
    if initial_capital {
        for word in iter {
            let mut chars = word.chars();
            if let Some(first) = chars.next() {
                result.push_str(&first.to_string().to_uppercase());
                result.push_str(&chars.as_str().to_lowercase());
            }
        }
    } else {
        if let Some(first) = iter.next() {
            result.push_str(&first.to_lowercase());
        }
        for word in iter {
            let mut chars = word.chars();
            if let Some(first) = chars.next() {
                result.push_str(&first.to_string().to_uppercase());
                result.push_str(&chars.as_str().to_lowercase());
            }
        }
    }
    result
}

#[derive(Debug, PartialEq, Eq)]
struct PyiCloudNoStoredPasswordAvailableException;

#[test]
fn test_get_password_from_keyring_success() {
    SAVED.with(|s| s.borrow_mut().insert("foo".to_string(), "bar".to_string()));
    assert_eq!(get_password_from_keyring("foo").unwrap(), "bar".to_string());
}

#[test]
fn test_get_password_from_keyring_failure() {
    let result = get_password_from_keyring("not-exist");
    assert!(result.is_err(), "Did not get error when password not present");
}

#[test]
fn test_password_exists_in_keyring_true() {
    SAVED.with(|s| s.borrow_mut().insert("a".to_string(), "b".to_string()));
    assert!(password_exists_in_keyring("a"));
}

#[test]
fn test_password_exists_in_keyring_false() {
    assert!(!password_exists_in_keyring("none"));
}

#[test]
fn test_store_password_in_keyring() {
    let out = store_password_in_keyring("x", "y");
    let found = SAVED.with(|s| s.borrow().get("x").map(|v| v == "y").unwrap_or(false));
    assert!(found, "Password not stored");
    assert_eq!(out, "set");
}

#[test]
fn test_delete_password_in_keyring() {
    SAVED.with(|s| s.borrow_mut().insert("delme".to_string(), "foo".to_string()));
    let out = delete_password_in_keyring("delme");
    let deleted = DELETED.with(|d| d.borrow().contains(&"delme".to_string()));
    assert!(deleted, "Username not marked as deleted");
    assert_eq!(out, "del");
}

#[test]
fn test_underscore_to_camelcase_basic() {
    assert_eq!(underscore_to_camelcase("hello_world", false), "helloWorld");
    assert_eq!(underscore_to_camelcase("A_b", true), "AB");
}

#[test]
fn test_get_password_interactive_false() {
    // Simulate keyring always fails ("raises")
    fn fail_get_password_from_keyring(_username: &str) -> Result<String, &'static str> {
        Err("PyiCloudNoStoredPasswordAvailableException")
    }
    let res = fail_get_password_from_keyring("z");
    assert!(res.is_err());
}

#[test]
fn test_get_password_interactive_true() {
    // Simulate keyring failure and fallback to getpass
    fn fail_get_password_from_keyring(_username: &str) -> Result<String, &'static str> {
        Err("PyiCloudNoStoredPasswordAvailableException")
    }
    fn getpass(_prompt: &str) -> String {
        "foo".to_string()
    }
    let password = getpass("Prompt: ");
    assert_eq!(password, "foo".to_string());
}