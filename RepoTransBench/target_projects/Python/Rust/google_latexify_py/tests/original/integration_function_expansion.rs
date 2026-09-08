// Translation of src/integration_tests/function_expansion_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_function_expansion_full() {
        fn f(x: i32) -> i32 { x * x }
        assert_eq!(f(5), 25);
    }
}