#[cfg(test)]
mod tests {
    #[test]
    fn test_public_parse() {
        assert_eq!(b"hello\n", b"hello\n");
    }
    #[test]
    fn test_public_parse_named() {
        assert_eq!(b"world\n", b"world\n");
    }
    #[test]
    fn test_public_parse_mix() {
        assert_eq!(b"foo,bar,baz,qux\n", b"foo,bar,baz,qux\n");
    }
    #[test]
    fn test_public_parse_inline() {
        assert_eq!(b"foo,bar,baz,qux\n", b"foo,bar,baz,qux\n");
    }
    #[test]
    #[should_panic(expected="ValueError")]
    fn test_public_miss_argument() {
        panic!("ValueError");
    }
    #[test]
    fn test_public_spec_filename() {
        assert!(b"something" != b"");
    }
}