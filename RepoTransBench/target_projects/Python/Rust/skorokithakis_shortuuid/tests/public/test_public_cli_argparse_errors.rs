#[cfg(test)]
mod tests {
    #[test]
    fn test_public_cli_fails_with_invalid_arg() {
        super::super::original::test_cli_argparse_errors::tests::test_cli_fails_with_invalid_arg();
    }
}