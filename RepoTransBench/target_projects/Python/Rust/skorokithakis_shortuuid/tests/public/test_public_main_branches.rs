#[cfg(test)]
mod tests {
    #[test]
    fn test_public_uuid_with_length() {
        super::super::original::test_main_branches::tests::test_uuid_with_length();
    }
    #[test]
    fn test_public_uuid_without_length() {
        super::super::original::test_main_branches::tests::test_uuid_without_length();
    }
    #[test]
    fn test_public_encode_decode_roundtrip() {
        super::super::original::test_main_branches::tests::test_encode_decode_roundtrip();
    }
    #[test]
    fn test_public_decode_invalid_error() {
        super::super::original::test_main_branches::tests::test_decode_invalid_error();
    }
}