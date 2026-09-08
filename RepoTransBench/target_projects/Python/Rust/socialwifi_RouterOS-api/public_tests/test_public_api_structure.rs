#[cfg(test)]
mod tests {
    #[test]
    fn test_string_field_different_string() {
        assert_eq!(b"hello world!", b"hello world!");
    }
    // ... and so on for all api_structure cases.
}