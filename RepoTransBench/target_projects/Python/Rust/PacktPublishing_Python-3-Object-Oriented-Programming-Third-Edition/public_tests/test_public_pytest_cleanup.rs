#[cfg(test)]
mod tests {
    struct DangerZone {
        code: String,
        is_clean: bool,
    }
    impl DangerZone {
        fn new(code: &str) -> Self {
            DangerZone { code: code.to_string(), is_clean: false }
        }
        fn clean(&mut self) {
            self.is_clean = true;
        }
    }
    #[test]
    fn test_cleanup_action_public() {
        let dz = DangerZone::new("DZ-909");
        assert!(!dz.is_clean);
    }
    #[test]
    fn test_cleanup_finalize_public() {
        let mut dz = DangerZone::new("DZ-909");
        dz.clean();
        assert!(dz.is_clean);
    }
}