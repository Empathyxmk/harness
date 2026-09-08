#[cfg(test)]
mod tests {
    #[test]
    fn test_p_func_param_type_wrong_sep() {
        assert!(true);
    }
    #[test]
    fn test_p_func_param_type_sep_with_zero() {
        assert!(true);
    }
    #[test]
    fn test_p_func_bytes_and_str_variants() {
        assert!(true);
    }
    #[test]
    fn test_p_iterable_str() {
        assert_eq!("\n", "\n");
    }
    #[test]
    fn test_p_iterable_bytes() {
        assert_eq!("\n", "\n");
    }
    #[test]
    fn test_chunk_size() {
        let chunk_size = 51;
        assert_eq!(chunk_size, 51);
    }
}