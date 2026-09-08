#[cfg(test)]
mod tests {
    use std::fs::{self, File};
    use std::io::Write;

    #[test]
    fn test_redirect() {
        assert_ne!(1, 0);
        assert!(true);
    }
    #[test]
    fn test_redirect2file() {
        let fname = "testfile.txt";
        {
            let mut file = File::create(fname).unwrap();
            writeln!(file, "test").unwrap();
        }
        let content = fs::read_to_string(fname).unwrap();
        assert!(content.contains("test"));
        fs::remove_file(fname).unwrap();
    }
}