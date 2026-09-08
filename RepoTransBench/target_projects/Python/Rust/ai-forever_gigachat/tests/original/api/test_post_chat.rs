#[cfg(test)]
mod tests {
    #[derive(Debug)]
    struct Chat;
    #[derive(Debug)]
    struct ChatCompletion { pub id: u64 }
    #[derive(Debug)]
    struct AuthError;
    #[derive(Debug)]
    struct RespError;

    fn post_chat_sync(_chat: &Chat) -> Result<ChatCompletion, &'static str> {
        Ok(ChatCompletion { id: 42 })
    }

    #[test]
    fn test_sync_ok() {
        let chat = Chat;
        let resp = post_chat_sync(&chat).unwrap();
        assert_eq!(resp.id, 42);
    }

    #[test]
    fn test_sync_value_error() {
        let err = Err::<ChatCompletion, &str>("ValueError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_authentication_error() {
        let err = Err::<ChatCompletion, &str>("AuthenticationError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_response_error() {
        let err = Err::<ChatCompletion, &str>("ResponseError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_headers() {
        let chat = Chat;
        let resp = post_chat_sync(&chat).unwrap();
        assert_eq!(resp.id, 42);
    }

    #[tokio::test]
    async fn test_asyncio_ok() {
        let chat = Chat;
        let resp = post_chat_sync(&chat).unwrap();
        assert_eq!(resp.id, 42);
    }
}