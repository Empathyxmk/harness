#[cfg(test)]
mod tests {
    use std::env;
    #[test]
    fn test_public_env_vars() {
        let envvars = env::vars().collect::<Vec<(String, String)>>();
        for (k, _) in &envvars {
            assert!(k.is_ascii());
        }
        let environ: Vec<(String, String)> = env::vars().collect();
        for (k, v) in environ {
            assert!(k.is_ascii());
            assert!(v.is_ascii());
        }
    }
}