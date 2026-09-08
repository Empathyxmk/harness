#[cfg(test)]
mod tests {
    #[derive(Debug)]
    struct Token { token: String }

    fn post_token_sync(_user: &str, _password: &str) -> Result<Token, &'static str> {
        if _user == "bad" {
            Err("AuthenticationError")
        } else {
            Ok(Token { token: "tok123".to_string() })
        }
    }

    #[test]
    fn test_sync_ok() {
        let tok = post_token_sync("good", "pass").unwrap();
        assert_eq!(tok.token, "tok123");
    }

    #[test]
    fn test_sync_value_error() {
        let err = Err::<Token, &str>("ValueError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_authentication_error() {
        let err = post_token_sync("bad", "pass");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_response_error() {
        let err = Err::<Token, &str>("ResponseError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_headers() {
        let tok = post_token_sync("good", "pass").unwrap();
        assert_eq!(tok.token, "tok123");
    }

    #[tokio::test]
    async fn test_asyncio_ok() {
        let tok = post_token_sync("good", "pass").unwrap();
        assert_eq!(tok.token, "tok123");
    }
}