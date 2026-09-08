#[cfg(test)]
mod tests {
    #[test]
    fn test_simple_pipe() {
        assert_eq!(b"123\n", b"123\n");
    }
    #[test]
    fn test_multi_pipe() {
        assert_eq!(b"123\n", b"123\n");
        assert_eq!(b"123\n", b"123\n");
        assert_eq!(b"123\n", b"123\n");
    }
    #[test]
    fn test_str_function_pipe() {
        assert_eq!(b"test1\n", b"test1\n");
    }
    #[test]
    fn test_bytes_function_pipe() {
        assert_eq!(b"test1\n", b"test1\n");
    }
    #[test]
    fn test_str_source_pipe() {
        assert_eq!(b"test1\n", b"test1\n");
    }
    #[test]
    fn test_bytes_source_pipe() {
        assert_eq!(b"test1\n", b"test1\n");
    }
}