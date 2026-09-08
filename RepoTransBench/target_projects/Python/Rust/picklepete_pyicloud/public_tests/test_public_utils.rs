use std::collections::HashMap;
use std::cell::RefCell;
use std::rc::Rc;

thread_local! {
    static SAVED: RefCell<HashMap<String, String>> = RefCell::new(HashMap::new());
    static DELETED: RefCell<Vec<String>> = RefCell::new(Vec::new());
}

struct PublicDummyKeyring;

impl PublicDummyKeyring {
    fn get_password(system: &str, username: &str) -> Option<String> {
        SAVED.with(|s| s.borrow().get(username).cloned())
    }
    fn set_password(system: &str, username: &str, password: &str) -> &'static str {
        SAVED.with(|s| s.borrow_mut().insert(username.to_string(), password.to_string()));
        "store"
    }
    fn delete_password(system: &str, username: &str) -> &'static str {
        DELETED.with(|d| d.borrow_mut().push(username.to_string()));
        "removed"
    }
}

fn get_password_from_keyring(username: &str) -> Result<String, &'static str> {
    PublicDummyKeyring::get_password("icloud", username).ok_or("PyiCloudNoStoredPasswordAvailableException")
}

fn password_exists_in_keyring(username: &str) -> bool {
    PublicDummyKeyring::get_password("icloud", username).is_some()
}

fn store_password_in_keyring(username: &str, password: &str) -> &'static str {
    PublicDummyKeyring::set_password("icloud", username, password)
}

fn delete_password_in_keyring(username: &str) -> &'static str {
    PublicDummyKeyring::delete_password("icloud", username)
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

#[test]
fn test_get_password_from_keyring_success() {
    SAVED.with(|s| s.borrow_mut().insert("baz".to_string(), "qux".to_string()));
    assert_eq!(get_password_from_keyring("baz").unwrap(), "qux".to_string());
}

#[test]
fn test_get_password_from_keyring_failure() {
    let result = get_password_from_keyring("does-not-exist");
    assert!(result.is_err());
}

#[test]
fn test_password_exists_in_keyring_true() {
    SAVED.with(|s| s.borrow_mut().insert("public_user".to_string(), "public_pw".to_string()));
    assert!(password_exists_in_keyring("public_user"));
}

#[test]
fn test_password_exists_in_keyring_false() {
    assert!(!password_exists_in_keyring("anonymous"));
}

#[test]
fn test_store_password_in_keyring() {
    let out = store_password_in_keyring("user2", "passwd2");
    let found = SAVED.with(|s| s.borrow().get("user2").map(|v| v == "passwd2").unwrap_or(false));
    assert!(found, "Password not stored in keyring");
    assert_eq!(out, "store");
}

#[test]
fn test_delete_password_in_keyring() {
    SAVED.with(|s| s.borrow_mut().insert("deleteme".to_string(), "secret".to_string()));
    let out = delete_password_in_keyring("deleteme");
    let deleted = DELETED.with(|d| d.borrow().contains(&"deleteme".to_string()));
    assert!(deleted);
    assert_eq!(out, "removed");
}

#[test]
fn test_underscore_to_camelcase_basic() {
    assert_eq!(underscore_to_camelcase("foo_bar_baz", false), "fooBarBaz");
    assert_eq!(underscore_to_camelcase("Bar_c", true), "BarC");
}

#[test]
fn test_get_password_interactive_false() {
    fn fail_get_password_from_keyring(_username: &str) -> Result<String, &'static str> {
        Err("PyiCloudNoStoredPasswordAvailableException")
    }
    let res = fail_get_password_from_keyring("userx");
    assert!(res.is_err());
}

#[test]
fn test_get_password_interactive_true() {
    fn fail_get_password_from_keyring(_username: &str) -> Result<String, &'static str> {
        Err("PyiCloudNoStoredPasswordAvailableException")
    }
    fn getpass(_prompt: &str) -> String {
        "public_secret".to_string()
    }
    let out = getpass("Prompt: ");
    assert_eq!(out, "public_secret");
}