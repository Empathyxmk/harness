// test_public_subuser_client.rs

#[cfg(test)]
mod tests {
    struct DummySubuserClientPublic {
        pub api_key: Option<String>,
        pub secret_key: Option<String>,
    }

    impl DummySubuserClientPublic {
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
            if sub_uid == Some(-1) {
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
            "done"
        }
    }

    #[test]
    fn test_post_set_subuser_transferability_true() {
        let client = DummySubuserClientPublic::new(Some("public-key"), Some("public-secret"));
        let res = client.post_set_subuser_transferability(Some("abcd"), Some(true));
        assert!(res.is_ok());
        let arr = res.unwrap();
        assert_eq!(arr[0]["transferability"], serde_json::json!(true));
        assert_eq!(arr[0]["uid"], serde_json::json!("abcd"));
    }

    #[test]
    fn test_post_set_subuser_transferability_false() {
        let client = DummySubuserClientPublic::new(Some("public-key"), Some("public-secret"));
        let res = client.post_set_subuser_transferability(Some("efgh"), Some(false));
        assert!(res.is_ok());
        assert_eq!(res.unwrap()[0]["transferability"], serde_json::json!(false));
    }

    #[test]
    fn test_post_set_subuser_transferability_invalid() {
        let client = DummySubuserClientPublic::new(Some("public-key"), Some("public-secret"));
        // Simulate passing invalid with Option<bool> = None
        let res = client.post_set_subuser_transferability(Some("efgh"), None);
        assert!(res.is_err());
    }

    #[test]
    fn test_post_set_subuser_transferability_no_uid() {
        let client = DummySubuserClientPublic::new(Some("public-key"), Some("public-secret"));
        let res = client.post_set_subuser_transferability(None, Some(true));
        assert!(res.is_err());
    }

    #[test]
    fn test_get_sub_user_deposit_history_ok() {
        let client = DummySubuserClientPublic::new(Some("public-key"), Some("public-secret"));
        let res = client.get_sub_user_deposit_history(Some(555));
        assert!(res.is_ok());
        let val = res.unwrap();
        assert_eq!(val.print_object(), "done");
    }

    #[test]
    fn test_get_sub_user_deposit_history_not_found() {
        let client = DummySubuserClientPublic::new(Some("public-key"), Some("public-secret"));
        let res = client.get_sub_user_deposit_history(Some(-1));
        assert!(res.is_err());
    }

    #[test]
    fn test_post_subuser_apikey_generate_success() {
        let client = DummySubuserClientPublic::new(Some("public-key"), Some("public-secret"));
        let res = client.post_subuser_apikey_generate(Some("pub_otp"), 999, Some("pub_note"), "readWrite");
        assert!(res.is_ok());
        let val = res.unwrap();
        assert_eq!(val.print_object(), "done");
    }

    #[test]
    fn test_post_subuser_apikey_generate_missing() {
        let client = DummySubuserClientPublic::new(Some("public-key"), Some("public-secret"));
        let res = client.post_subuser_apikey_generate(Some(""), 999, Some(""), "readWrite");
        assert!(res.is_err());
        let res2 = client.post_subuser_apikey_generate(None, 999, Some("pub_note"), "readWrite");
        assert!(res2.is_err());
    }

    #[test]
    fn test_init() {
        let c = DummySubuserClientPublic::new(None, None);
        assert!(c.api_key.is_none());
        assert!(c.secret_key.is_none());
    }
}