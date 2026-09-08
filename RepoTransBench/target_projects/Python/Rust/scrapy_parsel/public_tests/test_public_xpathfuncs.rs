// Rust translation of public_tests/test_public_xpathfuncs.py

#[cfg(test)]
mod tests {
    use super::*;
    use crate::xpathfuncs;

    #[test]
    fn test_tokenize_basic() {
        let tokens = xpathfuncs::tokenize(" foo-bar baz-qux ");
        assert_eq!(tokens, vec!["foo-bar", "baz-qux"]);
    }

    #[test]
    fn test_tokenize_with_commas() {
        let tokens = xpathfuncs::tokenize("123, test, foo");
        assert_eq!(tokens, vec!["123,", "test,", "foo"]);
    }

    #[test]
    fn test_str_to_number() {
        assert_eq!(xpathfuncs::str_to_number("4321"), 4321);
        assert_eq!(xpathfuncs::str_to_number("0x1A"), 26);
    }

    #[test]
    fn test_split_argument() {
        assert_eq!(
            xpathfuncs::split_argument("foo,bar;baz"),
            vec!["foo", "bar", "baz"]
        );
    }

    #[test]
    #[should_panic]
    fn test_hex_digits_error() {
        xpathfuncs::hex_digits("xyz");
    }
}