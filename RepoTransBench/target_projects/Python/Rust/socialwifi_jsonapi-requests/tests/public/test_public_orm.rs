#[cfg(test)]
mod tests {
    use super::*;
    use crate::orm::*;

    #[test]
    fn test_public_model_repr() {
        let model = OrmModel::new("Account");
        assert_eq!(model.to_string(), "OrmModel(Account)".to_string());
    }

    #[test]
    fn test_public_field_list() {
        let mut model = OrmModel::new("Thingy");
        model.set_field("count", 123.into());
        assert!(model.fields().contains(&"count".to_string()));
    }
}