use libfixmath_rs::fract32::*;
#[test]
fn test_fract32_create() {
    // denominator <= numerator, should return 0xFFFFFFFF
    assert_eq!(fract32_create(10, 5), 0xFFFFFFFF);
    assert_eq!(fract32_create(100, 100), 0xFFFFFFFF);

    // normal division; denominator > numerator
    let result = fract32_create(5, 10);
    assert!(result <= 0xFFFFFFFF);

    // edge: denominator just above numerator
    let result = fract32_create(9, 10);
    assert!(result <= 0xFFFFFFFF);
}

#[test]
fn test_fract32_invert() {
    assert_eq!(fract32_invert(0), 0xFFFFFFFF);
    assert_eq!(fract32_invert(12345), 0xFFFFFFFF - 12345);
    assert_eq!(fract32_invert(0xFFFFFFFF), 0);
}

#[cfg(not(feature = "fixmath_no_64bit"))]
#[test]
fn test_fract32_usmul() {
    // Simple fraction: halve the value
    assert_eq!(fract32_usmul(100, 0x80000000), 50); // 0x80000000 ~ 0.5
    // Full scale
    assert_eq!(fract32_usmul(123456789, 0xFFFFFFFF), 123456789);
    // Zero
    assert_eq!(fract32_usmul(12345, 0), 0);
}

#[cfg(not(feature = "fixmath_no_64bit"))]
#[test]
fn test_fract32_smul() {
    // Positive
    assert_eq!(fract32_smul(100, 0x80000000), 50);
    // Negative
    assert_eq!(fract32_smul(-100, 0x80000000), -50);
    // Zero
    assert_eq!(fract32_smul(0, 0x80000000), 0);
}