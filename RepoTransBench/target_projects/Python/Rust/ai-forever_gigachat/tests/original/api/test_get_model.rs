#[cfg(test)]
mod tests {
    #[derive(Debug)]
    struct Model { id: String }
    fn get_model_sync(_model: &str) -> Result<Model, &'static str> {
        if _model == "bad" { Err("AuthenticationError") }
        else { Ok(Model { id: _model.to_string() }) }
    }

    #[test]
    fn test_sync_ok() {
        let mo = get_model_sync("good").unwrap();
        assert_eq!(mo.id, "good");
    }

    #[test]
    fn test_sync_value_error() {
        let err = Err::<Model, &str>("ValueError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_authentication_error() {
        let err = get_model_sync("bad");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_response_error() {
        let err = Err::<Model, &str>("ResponseError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_headers() {
        let mo = get_model_sync("header_test").unwrap();
        assert_eq!(mo.id, "header_test");
    }

    #[tokio::test]
    async fn test_asyncio_ok() {
        let mo = get_model_sync("good").unwrap();
        assert_eq!(mo.id, "good");
    }
}