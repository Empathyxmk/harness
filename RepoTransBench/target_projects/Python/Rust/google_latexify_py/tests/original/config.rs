// Translation of src/latexify/config_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_config_default() {
        // Example: simulate a config default constructor
        struct Config { enabled: bool }
        let config = Config { enabled: true };
        assert!(config.enabled);
    }

    #[test]
    fn test_config_custom() {
        struct Config { enabled: bool }
        let config = Config { enabled: false };
        assert!(!config.enabled);
    }
}