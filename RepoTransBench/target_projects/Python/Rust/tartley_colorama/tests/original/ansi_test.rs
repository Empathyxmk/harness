#[cfg(test)]
mod tests {
    #[test]
    fn test_fore_attributes() {
        assert_eq!(Fore::BLACK, "\x1b[30m");
        assert_eq!(Fore::RED, "\x1b[31m");
        // More tests replicating the original Python logic can be added here.
    }
}