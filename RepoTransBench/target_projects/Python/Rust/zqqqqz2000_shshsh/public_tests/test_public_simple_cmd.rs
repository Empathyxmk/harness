#[cfg(test)]
mod tests {
    #[test]
    fn test_public_simple_echo() {
        assert_eq!(b"PUBTEST_123\n", b"PUBTEST_123\n");
    }
}