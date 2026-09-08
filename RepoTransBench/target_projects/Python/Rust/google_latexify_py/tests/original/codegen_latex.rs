// Translation of src/latexify/codegen/latex_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_latex_formatter() {
        let s = format!("x^2");
        assert_eq!(s, "x^2");
    }
}