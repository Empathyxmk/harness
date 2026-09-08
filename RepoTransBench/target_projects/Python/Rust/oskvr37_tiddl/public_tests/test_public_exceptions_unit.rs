#[cfg(test)]
mod tests {
    use crate::exceptions::ApiError;
    use std::collections::HashMap;

    #[test]
    fn test_apierror_str_repr_fields_public() {
        let mut others = HashMap::new();
        let err = ApiError {
            status: 400,
            sub_status: Some(99),
            user_message: Some("bad request".to_string()),
            error_code: Some(1234),
            message: Some("err occurred".to_string()),
            others,
        };
        let s = format!("{}", err);
        let r = format!("{:?}", err);
        assert!(s.contains("400"));
        assert!(r.contains("bad request"));
        assert_eq!(err.status, 400);
        assert_eq!(err.error_code, Some(1234));
        assert_eq!(err.sub_status, Some(99));
        assert_eq!(err.user_message.as_ref().unwrap(), "bad request");
        assert_eq!(err.message.as_ref().unwrap(), "err occurred");
    }

    #[test]
    fn test_apierror_missing_fields_public() {
        let others = HashMap::new();
        let err = ApiError {
            status: 403,
            sub_status: None,
            user_message: Some("denied".to_string()),
            error_code: None,
            message: None,
            others,
        };
        assert_eq!(err.status, 403);
        assert_eq!(err.user_message.as_ref().unwrap(), "denied");
        assert!(err.sub_status.is_none() || err.sub_status == Some(0));
        let r = format!("{:?}", err);
        assert!(r.contains("userMessage"));
    }

    #[test]
    fn test_apierror_only_status_public() {
        let others = HashMap::new();
        let err = ApiError {
            status: 500,
            sub_status: None,
            user_message: None,
            error_code: None,
            message: None,
            others,
        };
        assert_eq!(err.status, 500);
    }

    #[test]
    fn test_apierror_with_other_kwargs_public() {
        let mut others = HashMap::new();
        others.insert("custom_field".to_string(), "xyz".to_string());
        others.insert("another".to_string(), "val".to_string());
        let err = ApiError{
            status: 321,
            sub_status: None,
            user_message: None,
            error_code: None,
            message: None,
            others,
        };
        assert!(err.others.contains_key("custom_field"));
        assert!(err.others.contains_key("another"));
        assert_eq!(err.others.get("custom_field").unwrap(), "xyz");
        assert_eq!(err.others.get("another").unwrap(), "val");
    }
}