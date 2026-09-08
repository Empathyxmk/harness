#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_discovery_feature() {
        struct Discovery {}
        impl Discovery {
            fn discover(&self, feature: &str) -> Result<String, &'static str> {
                if feature == "feature_a" {
                    Ok("FeatureA discovered".to_string())
                } else {
                    Err("Feature not found")
                }
            }
        }

        let discovery = Discovery {};
        let result = discovery.discover("feature_a").unwrap();
        assert_eq!(result, "FeatureA discovered");
    }

    #[test]
    fn test_discovery_failure() {
        struct Discovery {}
        impl Discovery {
            fn discover(&self, feature: &str) -> Result<String, &'static str> {
                if feature == "feature_a" {
                    Ok("FeatureA discovered".to_string())
                } else {
                    Err("Feature not found")
                }
            }
        }

        let discovery = Discovery {};
        let result = discovery.discover("feature_b");
        assert!(result.is_err());
    }
}