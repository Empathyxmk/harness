#[cfg(test)]
mod tests {
    #[test]
    fn test_always_true() {
        // Equivalent to 'ck_assert_int_eq(2, 2)'
        assert_eq!(2, 2, "Public always true test with different numbers");
    }
}