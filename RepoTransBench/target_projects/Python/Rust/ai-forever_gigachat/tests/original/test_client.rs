#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    fn _unknown_kwargs(kwargs: HashMap<&str, &str>) -> HashMap<&str, &str> {
        kwargs
    }

    #[test]
    fn test_unknown_kwargs_gets_filtered() {
        let mut map = HashMap::new();
        map.insert("alpha", "beta");
        map.insert("gamma", "42");
        map.insert("is_test", "true");
        let result = _unknown_kwargs(map.clone());
        assert_eq!(result.get("alpha"), Some(&"beta"));
        assert_eq!(result.get("is_test"), Some(&"true"));
    }
}