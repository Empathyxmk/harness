#[cfg(test)]
mod tests {
    use fernet_fields_rs::FernetField;

    #[test]
    fn test_fernetfield_encrypt_decrypt() {
        let field = FernetField::new();
        let data = b"SensitiveData123";
        let encrypted = field.get_prep_value(data);
        let decrypted = field.from_db_value(&encrypted);
        assert_eq!(decrypted, data);
    }

    #[test]
    fn test_fernetfield_different_data() {
        let field = FernetField::new();
        let value = b"AnotherSecret";
        let encrypted = field.get_prep_value(value);
        let decrypted = field.from_db_value(&encrypted);
        assert_eq!(decrypted, value);
    }

    #[test]
    fn test_fernetfield_handles_empty_bytes() {
        let field = FernetField::new();
        let value = b"";
        let encrypted = field.get_prep_value(value);
        let decrypted = field.from_db_value(&encrypted);
        assert_eq!(decrypted, b"");
    }

    #[test]
    fn test_fernetfield_parametrize_1() {
        let val = b"param_1";
        let field = FernetField::new();
        let encrypted = field.get_prep_value(val);
        let decrypted = field.from_db_value(&encrypted);
        assert_eq!(decrypted, val);
    }

    #[test]
    fn test_fernetfield_parametrize_2() {
        let val = b"param_2";
        let field = FernetField::new();
        let encrypted = field.get_prep_value(val);
        let decrypted = field.from_db_value(&encrypted);
        assert_eq!(decrypted, val);
    }

    #[test]
    fn test_fernetfield_parametrize_3() {
        let val = b"param_3";
        let field = FernetField::new();
        let encrypted = field.get_prep_value(val);
        let decrypted = field.from_db_value(&encrypted);
        assert_eq!(decrypted, val);
    }
}