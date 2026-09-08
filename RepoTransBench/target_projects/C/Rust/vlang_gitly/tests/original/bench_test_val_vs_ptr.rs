// Translated from v_install/v/vlib/v/tests/bench/test_val_vs_ptr.c

#[cfg(test)]
mod tests {
    // Simulate C-style increment_val and increment_ptr.

    fn increment_val(n: i32) -> i32 {
        // Behaves as: return n + 2;
        n + 2
    }

    fn increment_ptr(n: &mut i32) {
        // Behaves as: *n = *n + 2;
        *n += 2;
    }

    #[test]
    fn test_increment_val() {
        assert_eq!(increment_val(3), 5);
        assert_eq!(increment_val(-2), 0);
    }

    #[test]
    fn test_increment_ptr() {
        let mut n = 10;
        increment_ptr(&mut n);
        assert_eq!(n, 12);
        n = -4;
        increment_ptr(&mut n);
        assert_eq!(n, -2);
    }
}