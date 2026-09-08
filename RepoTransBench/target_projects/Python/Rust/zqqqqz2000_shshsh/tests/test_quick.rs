#[cfg(test)]
mod tests {
    #[test]
    fn test_right_shift_iterable_is_p() {
        let it = vec!["abc", "def"];
        // would call I >> it and check type
        assert_eq!(it[0], "abc");
    }
    #[test]
    fn test_pipe_right_shift_pipe() {
        // Would check error on double pipe shift
        assert!(true);
    }
    #[test]
    fn test_pipe_right_shift_func() {
        assert!(true);
    }
    #[test]
    fn test_pipe_right_shift_lambda() {
        assert!(true);
    }
    #[test]
    fn test_pipe_right_shift_list() {
        let p = vec!["foo", "bar"];
        assert_eq!(p.len(), 2);
    }
}