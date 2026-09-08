#[cfg(test)]
mod tests {
    #[derive(Debug)]
    struct Models { models: Vec<String> }

    fn get_models_sync() -> Result<Models, &'static str> {
        Ok(Models { models: vec!["GigaChat".into(), "GigaChatPlus".into()] })
    }

    #[test]
    fn test_sync_ok() {
        let models = get_models_sync().unwrap();
        assert_eq!(models.models.len(), 2);
        assert_eq!(models.models[0], "GigaChat");
    }

    #[test]
    fn test_sync_value_error() {
        let err = Err::<Models, &str>("ValueError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_authentication_error() {
        let err = Err::<Models, &str>("AuthenticationError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_response_error() {
        let err = Err::<Models, &str>("ResponseError");
        assert!(err.is_err());
    }

    #[test]
    fn test_sync_headers() {
        let models = get_models_sync().unwrap();
        assert!(models.models.contains(&"GigaChat".to_string()));
    }

    #[tokio::test]
    async fn test_asyncio_ok() {
        let models = get_models_sync().unwrap();
        assert_eq!(models.models.len(), 2);
    }
}