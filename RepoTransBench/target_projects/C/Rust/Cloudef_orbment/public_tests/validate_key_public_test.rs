// Translated from tests/validate_key_public_test.c

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
fn test_validate_key_valid_public() {
    assert!(validate_key(Some("USERNAME8")));
}

#[test]
fn test_validate_key_empty_public() {
    assert!(!validate_key(Some("")));
}

#[test]
fn test_validate_key_null_public() {
    assert!(!validate_key(None));
}

#[test]
fn test_validate_key_long_public() {
    let key = "ABCDEFGHIJKLMNOPQR";
    assert!(key.len() > 16);
    assert!(!validate_key(Some(key)));
}

#[test]
fn test_validate_key_badchar_public() {
    assert!(!validate_key(Some("VALID!KEY")));
}