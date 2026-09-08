#[cfg(test)]
mod tests {
    #[test]
    fn test_simple_skip_public() {
        let test_platform = std::env::consts::OS;
        if test_platform != "fakeos" {
            // Simulate skip
            return;
        }
        assert!(false, "Should not reach here");
    }

    #[test]
    fn test_python38_public() {
        let n = "42".parse::<i32>().unwrap();
        assert_eq!(n, 42);
    }
}