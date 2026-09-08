#[cfg(test)]
mod tests {
    use super::*;
    use crate::request_factory::*;

    #[test]
    fn test_factory_defaults() {
        let params = std::collections::HashMap::new();
        let factory = crate::configuration::Factory::new(params);
        let conf = factory.create();
        assert_eq!(conf.api_root, "");
        assert_eq!(conf.retries, 1);
        assert_eq!(conf.validate_ssl, true);
        assert_eq!(conf.append_slash, false);
        assert_eq!(conf.timeout, None);
    }
}