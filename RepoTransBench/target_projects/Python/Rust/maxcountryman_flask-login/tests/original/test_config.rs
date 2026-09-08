#[cfg(test)]
mod tests {
    use crate::config::*;

    #[test]
    fn test_config_values() {
        assert_eq!(COOKIE_NAME, "remember_token");
        assert_eq!(COOKIE_DURATION.as_secs() / 86400, 365);
        assert!(!COOKIE_SECURE);
        assert!(COOKIE_HTTPONLY);
        assert!(EXEMPT_METHODS.iter().any(|x| x == "OPTIONS"));
        assert_eq!(LOGIN_MESSAGE, "Please log in to access this page.");
        assert_eq!(LOGIN_MESSAGE_CATEGORY, "message");
        assert_eq!(REFRESH_MESSAGE, "Please reauthenticate to access this page.");
        assert_eq!(REFRESH_MESSAGE_CATEGORY, "message");
        assert_eq!(ID_ATTRIBUTE, "get_id");
        assert!(SESSION_KEYS.contains("_user_id"));
        assert!(SESSION_KEYS.contains("_remember"));
        assert!(!USE_SESSION_FOR_NEXT);
    }
}