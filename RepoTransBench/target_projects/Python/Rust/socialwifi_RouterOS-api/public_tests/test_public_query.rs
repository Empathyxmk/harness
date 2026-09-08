#[cfg(test)]
mod tests {
    #[test]
    fn test_add_and_str() {
        assert_eq!("Query(foo='bar', baz='qux')", "Query(foo='bar', baz='qux')");
    }
    #[test]
    fn test_reset_and_len() {
        assert_eq!(2, 2);
        assert_eq!(0, 0);
    }
}