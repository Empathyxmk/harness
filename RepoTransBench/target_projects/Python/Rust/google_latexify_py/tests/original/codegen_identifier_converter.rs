// Translation of src/latexify/codegen/identifier_converter_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_identifier_converter() {
        let orig = "alpha_beta";
        let converted = orig.replace("_", "\\_");
        assert_eq!(converted, "alpha\\_beta");
    }
}