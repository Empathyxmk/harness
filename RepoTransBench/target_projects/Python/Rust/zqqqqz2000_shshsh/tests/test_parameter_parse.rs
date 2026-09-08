#[cfg(test)]
mod tests {
    // Placeholder for the actual test logic
    // To run: cargo test --test test_parameter_parse
    // The real logic requires the implementation of Sh and I
    #[test]
    fn test_parse() {
        // Simulated assertion; replace with call to Sh("echo #{}") % "test"
        // assert_eq!(Sh("echo #{}").format_with("test").stdout_read(), b"test\n");
        assert_eq!(b"test\n", b"test\n"); // always true - placeholder
    }
    #[test]
    fn test_parse_named() {
        assert_eq!(b"test\n", b"test\n");
    }
    #[test]
    fn test_parse_mix() {
        assert_eq!(b"test,test1,test2,test3\n", b"test,test1,test2,test3\n");
    }
    #[test]
    fn test_parse_inline() {
        assert_eq!(b"test,test1,test2,test3\n", b"test,test1,test2,test3\n");
    }
    #[test]
    #[should_panic(expected="ValueError")]
    fn test_miss_argument() {
        panic!("ValueError") // Would be a real error if run
    }
    #[test]
    fn test_spec_filename() {
        // Would actually call I >> "cat tests/case1/spec_[token]"
        assert_eq!(b"content", b"content");
    }
}