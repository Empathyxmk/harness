use venmo_business_rules::variables;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_public_variable_access() {
        let value = variables::get_variable("public_variable");
        assert!(value.is_some(), "Expected 'public_variable' to exist in the variables store.");
    }

    #[test]
    fn test_public_variable_default_value() {
        let value = variables::get_variable("default_variable").unwrap();
        assert_eq!(value, "default_value", "Default variable value should be 'default_value'.");
    }
}