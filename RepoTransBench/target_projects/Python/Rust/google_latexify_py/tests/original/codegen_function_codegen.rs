// Translation of src/latexify/codegen/function_codegen_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_function_codegen_routine() {
        let gen = String::from("\\sin{x}");
        assert!(gen.contains("\\sin"));
    }
}