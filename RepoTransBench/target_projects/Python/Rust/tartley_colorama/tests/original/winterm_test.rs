#[cfg(test)]
mod tests {
    #[test]
    fn test_winterm_functions() {
        let winterm = Winterm::new();
        assert!(winterm.functions_tested());
    }
}