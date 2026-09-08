#[cfg(test)]
mod tests {
    use super::*;
    use crate::orm::*;

    #[test]
    fn test_model_creation() {
        // Simulate creation and field access
        let mut model = OrmModel::new("User");
        model.set_field("id", 42.into());
        model.set_field("name", "Alice".into());
        assert_eq!(model.get_field("id"), Some(&42.into()));
        assert_eq!(model.get_field("name"), Some(&"Alice".into()));
    }

    #[test]
    fn test_model_serialization() {
        let mut model = OrmModel::new("Thing");
        model.set_field("foo", "bar".into());
        let json = model.to_json();
        assert!(json.contains("\"foo\":\"bar\""));
    }

    #[test]
    fn test_registry_add_and_lookup() {
        let mut reg = OrmRegistry::new();
        reg.register_model("User");
        assert!(reg.is_registered("User"));
        assert!(!reg.is_registered("Admin"));
    }
}