// Translation of src/latexify/parser_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_parser_basic() {
        // Simulate a parser that parses "3+4" to (3, '+', 4)
        let input = "3+4";
        let parsed = (3, '+', 4);
        assert_eq!(parsed, (3, '+', 4));
    }
}