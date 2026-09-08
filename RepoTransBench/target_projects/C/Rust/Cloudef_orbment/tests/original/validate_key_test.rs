// Translated from tests/validate_key_test.c

fn validate_key(key: Option<&str>) -> bool {
    match key {
        None => false,
        Some(k) => {
            let len = k.len();
            if len == 0 || len > 16 {
                return false;
            }
            k.chars().all(|c| c.is_ascii_alphanumeric())
        }
    }
}

#[test]
fn test_validate_key_valid() {
    assert!(validate_key(Some("KEY123")));
}

#[test]
fn test_validate_key_empty() {
    assert!(!validate_key(Some("")));
}

#[test]
fn test_validate_key_null() {
    assert!(!validate_key(None));
}

#[test]
fn test_validate_key_long() {
    let key = "ABCDEFGHIJKLMNOPQ";
    assert!(key.len() > 16);
    assert!(!validate_key(Some(key)));
}

#[test]
fn test_validate_key_badchar() {
    assert!(!validate_key(Some("KEY$123")));
}