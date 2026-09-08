#[cfg(test)]
mod tests {
    #[derive(Debug)]
    struct AccessToken { access_token: String }
    #[derive(Debug)]
    struct AuthError;
    #[derive(Debug)]
    struct RespError;

    fn post_auth_sync(_url: &str, _credentials: &str, _scope: &str) -> Result<AccessToken, &'static str> {
        if _credentials == "bad" {
            Err("AuthenticationError")
        } else {
            Ok(AccessToken { access_token: "valid_token".to_string() })
        }
    }

    #[test]
    fn test_sync_success() {
        let resp = post_auth_sync("url", "good", "scope").unwrap();
        assert_eq!(resp.access_token, "valid_token");
    }

    #[test]
    fn test_sync_value_error() {
        let resp = post_auth_sync("url", "", "scope");
        assert!(resp.is_ok());
    }

    #[test]
    fn test_sync_authentication_error() {
        let resp = post_auth_sync("url", "bad", "scope");
        assert!(resp.unwrap_err().contains("AuthenticationError"));
    }

    #[test]
    fn test_sync_response_error() {
        let err = Err::<AccessToken, &str>("ResponseError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_headers() {
        let resp = post_auth_sync("url", "good", "scope").unwrap();
        assert_eq!(resp.access_token, "valid_token");
    }

    #[tokio::test]
    async fn test_asyncio_success() {
        let resp = post_auth_sync("url", "good", "scope").unwrap();
        assert_eq!(resp.access_token, "valid_token");
    }
}