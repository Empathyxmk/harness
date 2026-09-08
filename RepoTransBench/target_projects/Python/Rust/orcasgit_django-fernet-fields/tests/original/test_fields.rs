#[cfg(test)]
mod tests {
    use fernet_fields_rs::{EncryptedTextField, EncryptedCharField};
    #[test]
    fn test_encrypted_field() {
        let value = "Secret Data";
        let field = EncryptedTextField::new();
        let enc = field.get_prep_value(value);
        let dec = field.from_db_value(&enc);
        assert_eq!(dec, value);
    }

    #[test]
    fn test_encrypted_char_field() {
        let value = "HelloWorld";
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
        let value = "the quick brown fox";
        let field = EncryptedTextField::new();
        let enc = field.get_prep_value(value);
        let dec = field.from_db_value(&enc);
        assert_eq!(dec, value);
    }

    #[test]
    fn test_encrypted_field_parametrize_2() {
        let value = "test_string_value";
        let field = EncryptedTextField::new();
        let enc = field.get_prep_value(value);
        let dec = field.from_db_value(&enc);
        assert_eq!(dec, value);
    }

    #[test]
    fn test_encrypted_field_parametrize_3() {
        let value = "another test message";
        let field = EncryptedTextField::new();
        let enc = field.get_prep_value(value);
        let dec = field.from_db_value(&enc);
        assert_eq!(dec, value);
    }
}