use system_bus_radio::implementations::mm_stream_si128::sbr_add;

#[test]
fn test_sbr_add_public() {
    // Simple addition with different values
    assert_eq!(sbr_add(10, 5), 15);
    // Negative numbers with different values
    assert_eq!(sbr_add(-7, -2), -9);
    // Addition with zero, swapped order
    assert_eq!(sbr_add(0, 12), 12);
    // Commutativity with different values
    assert_eq!(sbr_add(8, 3), sbr_add(3, 8));
    println!("All sbr_add PUBLIC tests passed.");
}