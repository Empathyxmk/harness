// Translation of public_tests/test_public_config.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_public_config_field() {
        struct Config { name: String }
        let cfg = Config { name: String::from("test") };
        assert_eq!(cfg.name, "test");
    }
}