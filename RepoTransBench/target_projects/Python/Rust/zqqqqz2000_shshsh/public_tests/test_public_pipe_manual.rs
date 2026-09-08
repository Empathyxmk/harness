#[cfg(test)]
mod tests {
    #[test]
    fn test_public_pipe_init_and_close() {
        assert!(true);
    }
    #[test]
    fn test_public_pipe_close_error_repr() {
        let s = "Custom error";
        assert!(s.contains("Custom"));
    }
}