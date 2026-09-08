#[cfg(test)]
mod tests {
    use std::fs::{self, File};
    use std::io::Write;
    use tempfile::TempDir;

    #[test]
    fn test_public_redirect_stdout() {
        let tmp = TempDir::new().unwrap();
        let f = tmp.path().join("pub_file.txt");
        {
            let mut file = File::create(&f).unwrap();
            writeln!(file, "8765").unwrap();
        }
        let content = fs::read_to_string(&f).unwrap();
        assert!(content.contains("8765"));
    }
}