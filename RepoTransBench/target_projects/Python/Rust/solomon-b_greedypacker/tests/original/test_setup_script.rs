#[cfg(test)]
mod tests {
    use std::fs;
    #[test]
    fn test_setup_file_exists_and_has_setuptools() {
        let path = "setup.py";
        let content = fs::read_to_string(path);
        assert!(content.is_ok(), "setup.py does not exist");
        if let Ok(text) = content {
            assert!(text.contains("setuptools"), "setup.py does not mention setuptools");
        }
    }
}