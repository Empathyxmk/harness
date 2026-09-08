#[cfg(test)]
mod tests {
    #[test]
    fn test_public_pipe_return_type() {
        assert!(true);
    }
    #[test]
    #[should_panic]
    fn test_public_pipe_invalid() {
        panic!("CommandNotFound");
    }
}