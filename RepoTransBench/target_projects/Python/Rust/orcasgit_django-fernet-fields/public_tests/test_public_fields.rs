use fernet_fields_rs::{EncryptedTextField, EncryptedCharField};

#[test]
fn test_encrypted_field_basic() {
    let value = "This is secret data for pub";
    let field = EncryptedTextField::new();
    let enc = field.get_prep_value(value);
    let dec = field.from_db_value(&enc);
    assert_eq!(dec, value);
}

#[test]
fn test_encrypted_char_field() {
    let value = "AlphaBravo";
    let field = EncryptedCharField::new(32);
    let enc = field.get_prep_value(value);
    let dec = field.from_db_value(&enc);
    assert_eq!(dec, value);
}

#[test]
fn test_encrypted_field_empty_string() {
    let value = "";
    let field = EncryptedTextField::new();
    let enc = field.get_prep_value(value);
    let dec = field.from_db_value(&enc);
    assert_eq!(dec, "");
}

#[test]
fn test_encrypted_field_parametrize_1() {
    let val = "fox jumps over the lazy dog";
    let field = EncryptedTextField::new();
    let enc = field.get_prep_value(val);
    let dec = field.from_db_value(&enc);
    assert_eq!(dec, val);
}

#[test]
fn test_encrypted_field_parametrize_2() {
    let val = "crazy_test_value_PUBLIC_CASE";
    let field = EncryptedTextField::new();
    let enc = field.get_prep_value(val);
    let dec = field.from_db_value(&enc);
    assert_eq!(dec, val);
}

#[test]
fn test_encrypted_field_parametrize_3() {
    let val = "another secret message";
    let field = EncryptedTextField::new();
    let enc = field.get_prep_value(val);
    let dec = field.from_db_value(&enc);
    assert_eq!(dec, val);
}