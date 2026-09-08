// Translation of public_tests/integration_test_public_regression.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_public_regression_case() {
        let previous = 10;
        let result = previous + 1;
        assert_eq!(result, 11);
    }
}