// This test assumes a config::from_str implemented in src/config.rs
#[cfg(test)]
mod tests {
    use crate::config;

    #[test]
    fn test_load_cfg_yaml_and_py() {
        // Case 1: YAML map with non-string keys should error in Rust (unlike Python's PyYAML)
        let yaml_bad = "1: 'foo'";
        let cfg_err = config::from_str(yaml_bad);
        assert!(cfg_err.is_err(), "YAML with non-string keys must fail to parse in Rust");

        // Case 2: YAML with valid string keys
        let yaml_ok = "foo: 'bar'\nanswer: 42";
        let cfg_ok = config::from_str(yaml_ok);
        assert!(cfg_ok.is_ok(), "YAML with string keys should parse successfully");
        let cfg = cfg_ok.unwrap();
        assert_eq!(cfg.get("foo").unwrap(), "bar");
        assert_eq!(cfg.get("answer").unwrap(), "42"); // assuming config API stores numeric as string, adjust if needed
    }
}