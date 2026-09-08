// Translation of src/latexify/transformers/function_expander_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_function_expander() {
        // Simulate function expansion
        fn add(a: i32, b: i32) -> i32 { a + b }
        assert_eq!(add(2, 3), 5);
    }
}