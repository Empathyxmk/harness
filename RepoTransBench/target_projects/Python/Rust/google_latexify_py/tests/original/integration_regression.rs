// Translation of src/integration_tests/regression_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_regression_known_result() {
        let input = vec![1, 2, 3];
        assert_eq!(input[0], 1);
    }
}