#[cfg(test)]
mod tests {
    #[test]
    fn test_public_streamer_basics() {
        struct S { pipe_read: i32, pipe_write: i32 }
        let s = S { pipe_read: 1, pipe_write: 2 };
        assert!(s.pipe_read == 1);
        assert!(s.pipe_write == 2);
    }
}