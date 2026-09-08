// test_subuser_client.rs

#[cfg(test)]
mod tests {
    // Simulated client, like DummySubuserClient in source

    struct DummySubuserClient {
        pub api_key: Option<String>,
        pub secret_key: Option<String>,
    }

    impl DummySubuserClient {
        fn new(api_key: Option<&str>, secret_key: Option<&str>) -> Self {
            Self {
                api_key: api_key.map(|s| s.to_string()),
                secret_key: secret_key.map(|s| s.to_string()),
            }
        }

        fn post_set_subuser_transferability(
            &self,
            sub_uids: Option<&str>,
            transferability: Option<bool>,
        ) -> Result<Vec<std::collections::HashMap<String, serde_json::Value>>, String> {
            if sub_uids.is_none() {
                return Err("sub_uids required".to_string());
            }
            let transfer = transferability.ok_or_else(|| "transferability required".to_string())?;
            if !matches!(transfer, true | false) {
                return Err("transferability must be bool".to_string());
            }
            let mut map = std::collections::HashMap::new();
            map.insert("uid".to_string(), serde_json::json!(sub_uids.unwrap()));
            map.insert("success".to_string(), serde_json::json!(true));
            map.insert("transferability".to_string(), serde_json::json!(transfer));
            Ok(vec![map])
        }

        fn get_sub_user_deposit_history(
            &self,
            sub_uid: Option<i32>,
        ) -> Result<DepositResult, String> {
            if sub_uid == Some(0) {
                return Err("Not found".to_string());
            }
            Ok(DepositResult {})
        }

        fn post_subuser_apikey_generate(
            &self,
            otp_token: Option<&str>,
            _sub_uid: i32,
            note: Option<&str>,
            _permission: &str,
        ) -> Result<DepositResult, String> {
            if otp_token.is_none() || otp_token.unwrap().is_empty() || note.is_none() || note.unwrap().is_empty() {
                return Err("otp_token and note required".to_string());
            }
            Ok(DepositResult {})
        }
    }

    struct DepositResult;
    impl DepositResult {
        fn print_object(&self) -> &'static str {
            "printed"
        }
    }

    #[test]
    fn test_post_set_subuser_transferability_true() {
        let client = DummySubuserClient::new(Some("test-key"), Some("test-secret"));
        let res = client.post_set_subuser_transferability(Some("1234"), Some(true));
        assert!(res.is_ok());
        let arr = res.unwrap();
        assert_eq!(arr[0]["transferability"], serde_json::json!(true));
        assert_eq!(arr[0]["uid"], serde_json::json!("1234"));
    }

    #[test]
    fn test_post_set_subuser_transferability_false() {
        let client = DummySubuserClient::new(Some("test-key"), Some("test-secret"));
        let res = client.post_set_subuser_transferability(Some("999"), Some(false));
        assert!(res.is_ok());
        assert_eq!(res.unwrap()[0]["transferability"], serde_json::json!(false));
    }

    #[test]
    fn test_post_set_subuser_transferability_invalid() {
        let client = DummySubuserClient::new(Some("test-key"), Some("test-secret"));
        // Simulate passing invalid with Option<bool> = None (type check not possible in Rust at runtime like Python)
        let res = client.post_set_subuser_transferability(Some("999"), None);
        assert!(res.is_err());
    }

    #[test]
    fn test_post_set_subuser_transferability_no_uid() {
        let client = DummySubuserClient::new(Some("test-key"), Some("test-secret"));
        let res = client.post_set_subuser_transferability(None, Some(true));
        assert!(res.is_err());
    }

    #[test]
    fn test_get_sub_user_deposit_history_ok() {
        let client = DummySubuserClient::new(Some("test-key"), Some("test-secret"));
        let res = client.get_sub_user_deposit_history(Some(100));
        assert!(res.is_ok());
        let val = res.unwrap();
        assert_eq!(val.print_object(), "printed");
    }

    #[test]
    fn test_get_sub_user_deposit_history_not_found() {
        let client = DummySubuserClient::new(Some("test-key"), Some("test-secret"));
        let res = client.get_sub_user_deposit_history(Some(0));
        assert!(res.is_err());
    }

    #[test]
    fn test_post_subuser_apikey_generate_success() {
        let client = DummySubuserClient::new(Some("test-key"), Some("test-secret"));
        let res = client.post_subuser_apikey_generate(Some("otp"), 123, Some("note"), "readOnly");
        assert!(res.is_ok());
        let val = res.unwrap();
        assert_eq!(val.print_object(), "printed");
    }

    #[test]
    fn test_post_subuser_apikey_generate_missing() {
        let client = DummySubuserClient::new(Some("test-key"), Some("test-secret"));
        let res = client.post_subuser_apikey_generate(None, 123, Some(""), "readOnly");
        assert!(res.is_err());
        let res = client.post_subuser_apikey_generate(Some("otp"), 123, Some(""), "readOnly");
        assert!(res.is_err());
    }

    #[test]
    fn test_init() {
        let c = DummySubuserClient::new(None, None);
        assert!(c.api_key.is_none());
        assert!(c.secret_key.is_none());
    }
}