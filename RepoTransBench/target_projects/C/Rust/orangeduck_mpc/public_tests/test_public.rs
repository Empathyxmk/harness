use orangeduck_mpc;

#[cfg(test)]
mod tests {
    #[test]
    fn test_public_one() {
        assert!(101 > 20);
        assert_eq!(303, 3 * 101);
    }

    #[test]
    fn test_public_two() {
        assert!(1 != 2);
        assert!(22 != 7);
    }

    #[test]
    fn test_public_three() {
        assert_eq!(7 * 6, 42);
        assert_eq!(100 / 2, 50);
    }
}