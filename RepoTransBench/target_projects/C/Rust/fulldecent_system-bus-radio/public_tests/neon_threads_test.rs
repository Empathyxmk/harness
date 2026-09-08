use system_bus_radio::implementations::neon_threads::sbr_mul;

#[test]
fn test_sbr_mul_public() {
    // Simple multiplication with different values
    assert_eq!(sbr_mul(2, 7), 14);
    // Multiplying by zero with swapped operands
    assert_eq!(sbr_mul(0, 11), 0);
    // Multiplying negatives with different values
    assert_eq!(sbr_mul(-3, -5), 15);
    assert_eq!(sbr_mul(-4, 3), -12);
    // Commutativity with different values
    assert_eq!(sbr_mul(9, 2), sbr_mul(2, 9));
    println!("All sbr_mul PUBLIC tests passed.");
}