#[cfg(test)]
mod tests {
    use super::*;
    use crate::VERSION;

    #[test]
    fn test_fake_integration_public() {
        assert!(VERSION.starts_with("0."));
        assert_eq!(VERSION.chars().filter(|c| *c == '.').count(), 2);
    }
}