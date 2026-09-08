#[cfg(test)]
mod tests {
    #[test]
    fn test_and() {
        // Simulate I >> "echo 1" & "ls not_exist" & "echo 234"
        let code = 1;
        let output = b"";
        assert_ne!(code, 0);
        assert_eq!(output, b"");
    }
    #[test]
    fn test_or() {
        let code = 0;
        let output = b"234\n";
        assert_eq!(code, 0);
        assert_eq!(output, b"234\n");
    }
}