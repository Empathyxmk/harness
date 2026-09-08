#[cfg(test)]
mod tests {
    use tempfile::TempDir;
    use std::env;
    #[test]
    fn test_ch_cwd() {
        let orig_dir = env::current_dir().unwrap();
        let tmp = TempDir::new().unwrap();
        {
            let temp_path = tmp.path();
            env::set_current_dir(temp_path).unwrap();
            assert_eq!(env::current_dir().unwrap(), temp_path);
            // Restore
            env::set_current_dir(&orig_dir).unwrap();
        }
        assert_eq!(env::current_dir().unwrap(), orig_dir);
    }
}