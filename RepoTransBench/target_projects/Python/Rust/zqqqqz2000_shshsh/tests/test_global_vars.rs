#[cfg(test)]
mod tests {
    use std::env;

    #[test]
    fn test_cwd_env_exist() {
        let cwd = env::current_dir().unwrap();
        assert_eq!(cwd, env::current_dir().unwrap());
        let envvars = env::vars().collect::<Vec<(String, String)>>();
        for (k, v) in envvars {
            assert!(k.is_ascii() && v.is_ascii());
        }
    }
}