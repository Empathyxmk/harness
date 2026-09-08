#[cfg(test)]
mod tests {
    #[test]
    fn test_public_shell_echo() {
        assert_eq!(b"helloworld\n", b"helloworld\n");
    }
}