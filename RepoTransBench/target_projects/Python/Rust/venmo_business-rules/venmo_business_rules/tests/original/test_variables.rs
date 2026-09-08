use venmo_business_rules::variables;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_base_has_no_variables() {
        // Simulating the original Python logic
        let vars = variables::get_all_variables();
        assert_eq!(vars.len(), 0, "Base should not have any variables.");
    }

    #[test]
    fn test_get_all_variables() {
        // Simulating behavior based on Python logic
        let vars = variables::get_all_variables();
        assert!(vars.contains(&String::from("variable_a")), "Expected 'variable_a' in the list of variables.");
    }
}