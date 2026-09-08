#[cfg(test)]
mod tests {
    // Public version: Just call original test in integration
    #[test]
    fn test_public_cli_shows_help() {
        super::super::original::test_cli::tests::test_cli_shows_help();
    }
}