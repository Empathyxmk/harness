#[cfg(test)]
mod tests {
    #[test]
    fn test_is_alive() {
        fn is_alive() -> bool {
            true
        }

        assert!(is_alive());
    }
}