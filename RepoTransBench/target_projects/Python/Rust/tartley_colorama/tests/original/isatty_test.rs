#[cfg(test)]
mod tests {
    #[test]
    fn test_isatty_check() {
        assert!(isatty(std::io::stdout()));
    }
}