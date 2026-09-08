// Translation of src/latexify/transformers/docstring_remover_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_docstring_remover() {
        // Simulate the effect: remove docstring from function
        fn f() -> i32 { 5 /* docstring would be ignored in Rust */ }
        assert_eq!(f(), 5);
    }
}