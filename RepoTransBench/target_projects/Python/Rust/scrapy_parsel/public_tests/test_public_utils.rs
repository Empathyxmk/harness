// Rust translation of public_tests/test_public_utils.py

#[cfg(test)]
mod tests {
    use super::*;
    use crate::utils;

    #[test]
    fn test_to_unicode_int_input() {
        assert_eq!(utils::to_unicode(6789), "6789");
    }

    #[test]
    fn test_to_unicode_byte_input() {
        assert_eq!(utils::to_unicode(b"NewTest"), "NewTest");
    }

    #[test]
    fn test_to_unicode_str_input() {
        assert_eq!(utils::to_unicode("UnicodeStringTest"), "UnicodeStringTest");
    }

    #[test]
    #[should_panic]
    fn test_to_unicode_error() {
        struct A;
        utils::to_unicode(A);
    }
}