#[cfg(test)]
mod tests {
    use super::*;
    use crate::request_factory::*;

    #[test]
    fn test_factory_creates_api_config() {
        let mut params = std::collections::HashMap::new();
        params.insert("API_ROOT".to_string(), "https://api.example.com/".to_string());
        params.insert("RETRIES".to_string(), "2".to_string());
        let factory = crate::configuration::Factory::new(params);
        let conf = factory.create();
        assert_eq!(conf.api_root, "https://api.example.com/");
        assert_eq!(conf.retries, 2);
        assert_eq!(conf.validate_ssl, true);
        assert_eq!(conf.append_slash, false);
        assert_eq!(conf.timeout, None);
    }
}