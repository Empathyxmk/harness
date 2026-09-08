#[cfg(test)]
mod tests {
    #[test]
    fn test_parsing_logic() {
        // Test parsing logic, e.g., JSON or other data format
        fn parse_data(input: &str) -> Result<i32, String> {
            input.parse::<i32>().map_err(|_| "Parsing error".into())
        }

        assert_eq!(parse_data("42"), Ok(42));
        assert_eq!(parse_data("abc"), Err(String::from("Parsing error")));
    }
}