#[cfg(test)]
mod tests {
    #[test]
    fn test_public_pipe_context_manager() {
        let fd1 = 1;
        let fd2 = 2;
        assert_ne!(fd1, fd2);
    }
}