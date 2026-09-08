use system_bus_radio::implementations::neon_threads::sbr_mul;

#[test]
fn test_mul_basic() {
    assert_eq!(sbr_mul(2, 3), 6);
    assert_eq!(sbr_mul(0, 10), 0);
    assert_eq!(sbr_mul(-2, 3), -6);
}

#[test]
fn test_mul_one() {
    assert_eq!(sbr_mul(1, 999), 999);
    assert_eq!(sbr_mul(-1, 7), -7);
}

#[test]
fn test_sbr_mul_extra() {
    // Simple multiplication
    assert_eq!(sbr_mul(3, 4), 12);
    // Multiplying by zero
    assert_eq!(sbr_mul(7, 0), 0);
    // Multiplying negatives
    assert_eq!(sbr_mul(-2, -4), 8);
    assert_eq!(sbr_mul(-2, 4), -8);
    // Commutativity
    assert_eq!(sbr_mul(5, 6), sbr_mul(6, 5));
}