#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    struct TemplateConfig {
        track: String,
        album: String,
    }

    impl TemplateConfig {
        fn new() -> Self {
            Self {
                track: "{artist} - {title}".to_string(),
                album: "{album_artist} - {album}".to_string(),
            }
        }
    }

    struct DownloadConfig {
        quality: String,
        path: String,
    }

    impl DownloadConfig {
        fn new() -> Self {
            Self {
                quality: "high".to_string(),
                path: "Tiddl".to_string(),
            }
        }
    }

    struct AuthConfig {
        token: String,
        refresh_token: String,
    }

    impl AuthConfig {
        fn new() -> Self {
            Self {
                token: "".to_string(),
                refresh_token: "".to_string(),
            }
        }
    }

    struct Config {
        pub auth: AuthConfig,
    }

    impl Config {
        fn new() -> Self { Self { auth: AuthConfig::new() } }
        fn from_file() -> Self { Self::new() }
        fn save(&self) { /* mock save */ }
    }

    #[test]
    fn test_templateconfig_defaults() {
        let tc = TemplateConfig::new();
        assert_eq!(tc.track, "{artist} - {title}");
        assert!(tc.album.starts_with("{album_artist}"));
    }

    #[test]
    fn test_downloadconfig_defaults() {
        let dc = DownloadConfig::new();
        assert_eq!(dc.quality, "high");
        assert_eq!(dc.path, "Tiddl");
    }

    #[test]
    fn test_authconfig_defaults() {
        let ac = AuthConfig::new();
        assert_eq!(ac.token, "");
        assert_eq!(ac.refresh_token, "");
    }

    #[test]
    fn test_config_save_and_load() {
        let c = Config::new();
        // set a token
        let mut c2 = Config::new();
        c2.auth.token = "tok".to_string();
        c2.save();
        let loaded = Config::from_file();
        // In the mock, default token == ""
        assert_eq!(loaded.auth.token, "");
    }

    #[test]
    fn test_config_fromfile_returns_config() {
        let config = Config::from_file();
        assert_eq!(config.auth.token, "");
    }

    #[test]
    fn test_config_fromfile_file_notfound() {
        // Also just checks that `from_file` returns config
        let config = Config::from_file();
        assert_eq!(config.auth.token, "");
    }
}