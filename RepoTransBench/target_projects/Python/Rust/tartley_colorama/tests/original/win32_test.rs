#[cfg(test)]
mod tests {
    #[test]
    fn test_win32_flags() {
        set_win32_flags();
        assert!(flags_set_correctly());
    }
}