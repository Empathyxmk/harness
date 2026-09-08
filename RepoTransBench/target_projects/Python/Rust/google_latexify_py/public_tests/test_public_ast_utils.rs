// Translation of public_tests/test_public_ast_utils.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_public_ast_utils_case() {
        let string = "abcde";
        assert!(string.contains("b"));
    }
}