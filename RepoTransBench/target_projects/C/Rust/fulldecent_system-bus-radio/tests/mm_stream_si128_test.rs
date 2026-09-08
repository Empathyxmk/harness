use system_bus_radio::implementations::mm_stream_si128::sbr_add;

#[test]
fn test_add_zero() {
    assert_eq!(sbr_add(0, 0), 0);
    assert_eq!(sbr_add(123, 0), 123);
    assert_eq!(sbr_add(0, 456), 456);
}

#[test]
fn test_add_negative() {
    assert_eq!(sbr_add(-1, -2), -3);
    assert_eq!(sbr_add(-10, 5), -5);
}

#[test]
fn test_sbr_add_extra() {
    // Simple addition
    assert_eq!(sbr_add(2, 3), 5);
    // Negative numbers
    assert_eq!(sbr_add(-2, -3), -5);
    // Addition with zero
    assert_eq!(sbr_add(7, 0), 7);
    // Commutativity
    assert_eq!(sbr_add(4, 9), sbr_add(9, 4));
}