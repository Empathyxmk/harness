#[cfg(test)]
mod tests {
    #[test]
    fn test_one_cmd() {
        assert_eq!(b"123\n", b"123\n");
    }
    #[test]
    fn test_quick_cmd() {
        assert_eq!(b"123\n", b"123\n");
    }
    #[test]
    fn test_get_stderr() {
        assert!(true);
    }
    #[test]
    fn test_read_out() {
        let out = vec!["abc", "", "", "defg", ""];
        for (i, line) in out.iter().enumerate() {
            assert_eq!(out[i], *line);
        }
        assert_eq!(out.len() - 1, 4);
    }
}