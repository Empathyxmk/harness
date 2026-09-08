#[cfg(test)]
mod tests {
    use super::super::super::src::util::*;

    #[test]
    fn test_random_string_length() {
        for n in [1, 5, 10, 32].iter().cloned() {
            let s = random_string(n);
            assert_eq!(s.len(), n);
        }
    }

    #[test]
    fn test_quote_string_basic() {
        assert_eq!(quote_string("abc"), "\"abc\"");
        assert_eq!(quote_string("he\"llo"), "\"he\\\"llo\"");
        assert_eq!(quote_string("back\\slash"), "\"back\\\\slash\"");
    }
}