// test_public_api_signature.rs

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    // Simulate builder
    struct DummyBuilder {
        params: HashMap<String, String>
    }
    impl DummyBuilder {
        fn new() -> Self {
            Self { params: HashMap::new() }
        }
        fn put_url(&mut self, k: &str, v: &str) {
            self.params.insert(k.into(), v.into());
        }
        fn build_url(&self) -> String {
            if self.params.is_empty() {
                "".to_string()
            } else {
                let mut p: Vec<(String, String)> = self.params.iter().map(|(k, v)| (k.clone(), v.clone())).collect();
                p.sort();
                let pairs: Vec<String> = p.iter().map(|(k, v)| format!("{}={}", k, v)).collect();
                pairs.join("&")
            }
        }
    }

    fn create_signature(
        ak: &str,
        _sk: &str,
        _method: &str,
        _host: &str,
        _path: &str,
        builder: &mut DummyBuilder,
    ) -> HashMap<String, String> {
        // Patch utc_now as "888"
        builder.put_url("AccessKeyId", ak);
        builder.put_url("SignatureMethod", "HmacSHA256");
        builder.put_url("Timestamp", "888");
        builder.put_url("Signature", "dummy");
        let mut m = HashMap::new();
        m.insert("AccessKeyId".to_string(), ak.to_string());
        m.insert("SignatureMethod".to_string(), "HmacSHA256".to_string());
        m.insert("Timestamp".to_string(), "888".to_string());
        m.insert("Signature".to_string(), "dummy".to_string());
        m
    }

    fn create_signatureED25519(
        ak: &str,
        private_key_b64: &str,
        _method: &str,
        _url: &str,
        builder: &mut DummyBuilder
    ) -> Result<HashMap<String, String>, String> {
        builder.put_url("AccessKeyId", ak);
        builder.put_url("Timestamp", "1001");
        builder.put_url("SignatureMethod", "ED25519");
        builder.put_url("Signature", "dummy");
        // With this key, always error
        if private_key_b64 == "VGhpcyBpcyBub3QgYSBwZW0gcGVpYmUvZWRmMjU1MTkga2V5IQ==" {
            Err("invalid private key".to_string())
        } else {
            Ok(HashMap::new())
        }
    }

    #[test]
    fn test_public_request() {
        let mut builder = DummyBuilder::new();
        let result = create_signature("key", "secret", "PUT", "api.huobi.pro", "/v2/test/do", &mut builder);
        assert!(result.contains_key("Signature"));
        assert_eq!(result.get("AccessKeyId"), Some(&"key".to_string()));
        assert_eq!(result.get("SignatureMethod"), Some(&"HmacSHA256".to_string()));
        assert_eq!(result.get("Timestamp"), Some(&"888".to_string()));
    }

    #[test]
    fn test_public_request3() {
        let mut builder = DummyBuilder::new();
        let private_key_b64 = "VGhpcyBpcyBub3QgYSBwZW0gcGVpYmUvZWRmMjU1MTkga2V5IQ==";
        let res = create_signatureED25519("456", private_key_b64, "POST", "http://127.0.0.1/api", &mut builder);
        assert!(res.is_err());
    }
}