// Translated from v_install/v/vlib/v/tests/test_global_init_test.v

#[cfg(test)]
mod tests {
    // Simulate initialization
    fn my_init() -> i32 {
        assert!(true);
        1
    }

    static X: once_cell::sync::Lazy<i32> = once_cell::sync::Lazy::new(|| my_init());

    #[test]
    fn test_my_init() {
        assert_eq!(*X, 1);
    }
}