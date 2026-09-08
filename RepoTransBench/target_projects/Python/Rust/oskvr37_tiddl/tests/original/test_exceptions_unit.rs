#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use crate::exceptions::ApiError;

    #[test]
    fn test_api_error_str_repr_fields() {
        let mut others = HashMap::new();
        let err = ApiError {
            status: 404,
            sub_status: Some(0),
            user_message: Some("not found".to_string()),
            error_code: Some(999),
            message: Some("msg".to_string()),
            others,
        };
        let s = format!("{}", err);
        let r = format!("{:?}", err);
        assert!(s.contains("404"));
        assert!(r.contains("not found"));
        assert_eq!(err.status, 404);
        assert_eq!(err.error_code, Some(999));
        assert_eq!(err.sub_status, Some(0));
        assert_eq!(err.user_message.as_ref().unwrap(), "not found");
        assert_eq!(err.message.as_ref().unwrap(), "msg");
    }

    #[test]
    fn test_api_error_missing_fields() {
        let others = HashMap::new();
        let err = ApiError {
            status: 401,
            sub_status: None,
            user_message: None,
            error_code: None,
            message: None,
            others,
        };
        assert_eq!(err.status, 401);
        assert!(err.sub_status.is_none() || err.sub_status == Some(0));
        let r = format!("{:?}", err);
        assert!(r.contains("userMessage"));
    }

    #[test]
    fn test_api_error_only_status() {
        let others = HashMap::new();
        let err = ApiError {
            status: 502,
            sub_status: None,
            user_message: None,
            error_code: None,
            message: None,
            others,
        };
        assert_eq!(err.status, 502);
    }

    #[test]
    fn test_api_error_with_kwargs() {
        let mut others = HashMap::new();
        others.insert("foo".to_string(), "bar".to_string());
        others.insert("custom".to_string(), "cval".to_string());
        let err = ApiError {
            status: 123,
            sub_status: None,
            user_message: None,
            error_code: None,
            message: None,
            others: others.clone(),
        };
        assert!(err.others.contains_key("foo"));
        assert!(err.others.contains_key("custom"));
        assert_eq!(&err.others["foo"], "bar");
        assert_eq!(&err.others["custom"], "cval");
    }
}