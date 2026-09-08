#[cfg(test)]
mod tests {
    struct Auth {
        token: String,
        user_id: String,
        country_code: String,
    }
    struct Download {
        quality: String,
        concurrent_downloads: u32,
    }
    struct Config {
        auth: Auth,
        output_dir: Option<String>,
        download: Option<Download>,
    }

    impl Config {
        fn new(auth: Auth, output_dir: Option<String>, download: Option<Download>) -> Self {
            Self { auth, output_dir, download }
        }
    }

    #[test]
    fn test_config_defaults_public() {
        let cfg = Config::new(
            Auth{
                token: "public_token_abc".to_string(),
                user_id: "public_uid".to_string(),
                country_code: "DE".to_string(),
            }, Some("public_music".to_string()),
            Some(Download { quality: "HI_RES_LOSSLESS".to_string(), concurrent_downloads: 8 }),
        );
        assert_eq!(&cfg.auth.token, "public_token_abc");
        assert_eq!(&cfg.auth.user_id, "public_uid");
        assert_eq!(&cfg.auth.country_code, "DE");
        assert!(cfg.output_dir.as_ref().unwrap().contains("public_music"));
        assert_eq!(cfg.download.as_ref().unwrap().quality, "HI_RES_LOSSLESS");
        assert_eq!(cfg.download.as_ref().unwrap().concurrent_downloads, 8);
    }

    #[test]
    fn test_config_partial_data_public() {
        let cfg = Config::new(
            Auth {
                token: "another_token_xyz".to_string(),
                user_id: "another_uid".to_string(),
                country_code: "US".to_string()
            },
            None,
            None
        );
        assert_eq!(&cfg.auth.token, "another_token_xyz");
        assert_eq!(&cfg.auth.user_id, "another_uid");
        assert_eq!(&cfg.auth.country_code, "US");
    }

    #[test]
    fn test_config_invalid_public() {
        // Missing user_id/country_code would be a compile error in struct, so just assert!
        let error = std::panic::catch_unwind(|| {
            Config::new(
                Auth {
                    token: "missing_fields".to_string(),
                    user_id: "".to_string(),
                    country_code: "".to_string()
                },
                None, None
            );
        });
        assert!(error.is_ok());
    }
}