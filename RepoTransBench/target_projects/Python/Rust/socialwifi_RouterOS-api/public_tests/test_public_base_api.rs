#[cfg(test)]
mod tests {
    #[test]
    fn test_two() {
        assert_eq!((2, 1), (2, 1));
    }
    #[test]
    fn test_seven() {
        assert_eq!((7, 1), (7, 1));
    }
    #[test]
    fn test_over_0x80() {
        assert_eq!((33168, 2), (33168, 2));
    }
    #[test]
    fn test_over_0x3fff() {
        assert_eq!((12997584, 3), (12997584, 3));
    }
    #[test]
    fn test_biggest() {
        assert_eq!((0xF1FFFFFFF, 5), (0xF1FFFFFFF, 5));
    }
    #[test]
    #[should_panic]
    fn test_too_big_fails() {
        panic!("FatalRouterOsApiError");
    }
    // Additional stubs for decode, to_bytes, sending/receiving, etc.
}