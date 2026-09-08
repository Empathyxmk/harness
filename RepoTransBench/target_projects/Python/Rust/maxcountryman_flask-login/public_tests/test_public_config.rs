#[cfg(test)]
mod tests {
    use crate::config::*;
    use std::time::Duration;

    #[test]
    fn test_cookie_name_public() {
        assert!(COOKIE_NAME.starts_with("remember"));
    }

    #[test]
    fn test_cookie_duration_public() {
        assert!(COOKIE_DURATION >= Duration::from_secs(60 * 60 * 24 * 300));
    }

    #[test]
    fn test_cookie_secure_public() {
        assert_eq!(COOKIE_SECURE, false);
    }

    #[test]
    fn test_cookie_httponly_public() {
        assert!(COOKIE_HTTPONLY);
    }

    #[test]
    fn test_cookie_samesite_public() {
        assert!(COOKIE_SAMESITE.is_none());
    }

    #[test]
    fn test_login_message_public() {
        assert!(LOGIN_MESSAGE.to_lowercase().contains("log in"));
    }

    #[test]
    fn test_login_message_category_public() {
        assert!(LOGIN_MESSAGE_CATEGORY.len() > 2);
    }

    #[test]
    fn test_refresh_message_public() {
        assert!(REFRESH_MESSAGE.starts_with("Please reauth"));
    }

    #[test]
    fn test_refresh_message_category_public() {
        assert_eq!(REFRESH_MESSAGE_CATEGORY, LOGIN_MESSAGE_CATEGORY);
    }

    #[test]
    fn test_id_attribute_public() {
        assert!(ID_ATTRIBUTE.ends_with("id"));
    }

    #[test]
    fn test_session_keys_public() {
        assert!(SESSION_KEYS.contains("_user_id"));
        assert!(SESSION_KEYS.contains("_id"));
    }

    #[test]
    fn test_exempt_methods_public() {
        assert!(EXEMPT_METHODS.iter().any(|x| x == "OPTIONS"));
    }

    #[test]
    fn test_use_session_for_next_public() {
        assert!(!USE_SESSION_FOR_NEXT);
    }
}