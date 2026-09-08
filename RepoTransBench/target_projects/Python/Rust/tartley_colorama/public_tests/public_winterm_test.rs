#[cfg(test)]
mod tests {
    #[test]
    fn test_winterm_public_functionality() {
        let winterm = Winterm::new();
        assert!(winterm.public_functionality_tested());
    }
}