#[cfg(test)]
mod tests {
    use std::env;
    #[test]
    fn test_public_cwd() {
        let cwd = env::current_dir().unwrap();
        assert_eq!(cwd, env::current_dir().unwrap());
    }
}