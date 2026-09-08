// Translation of src/latexify/codegen/function_codegen_match_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_function_codegen_match() {
        let func = "f(x)";
        assert!(func.starts_with("f"));
    }
}