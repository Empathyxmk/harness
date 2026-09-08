#[cfg(test)]
mod tests {
    use crate::exceptions::ApiError;
    use std::collections::HashMap;

    #[test]
    fn test_apierror_message_and_status_public() {
        let err = ApiError {
            status: 420,
            sub_status: None,
            user_message: Some("Slow Down".to_string()),
            error_code: None,
            message: Some("Enhance Your Calm".to_string()),
            others: HashMap::new(),
        };
        let s = format!("{}", err);
        assert!(s.contains("Enhance"));
        assert_eq!(err.status, 420);
        assert_eq!(err.user_message.as_ref().unwrap(), "Slow Down");
    }

    #[test]
    fn test_apierror_repr_has_all_fields_public() {
        let mut others = HashMap::new();
        let err = ApiError {
            status: 405,
            sub_status: Some(9),
            user_message: Some("Not Allowed".to_string()),
            error_code: Some(77),
            message: None,
            others,
        };
        let s = format!("{:?}", err);
        assert!(s.contains("errorCode"));
        assert!(s.contains("77"));
        assert!(s.contains("userMessage"));
        assert!(s.contains("Not Allowed"));
        assert!(s.contains("subStatus"));
        assert!(s.contains("9"));
    }
}