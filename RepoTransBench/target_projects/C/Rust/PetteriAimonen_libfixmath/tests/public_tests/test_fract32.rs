use libfixmath_rs::fract32::*;

#[test]
fn public_test_fract32_create() {
    assert_eq!(fract32_create(30, 10), 0xFFFFFFFF);
    assert_eq!(fract32_create(255, 255), 0xFFFFFFFF);

    let result = fract32_create(7, 13);
    assert!(result <= 0xFFFFFFFF);

    let result = fract32_create(50, 51);
    assert!(result <= 0xFFFFFFFF);
}

#[test]
fn public_test_fract32_invert() {
    assert_eq!(fract32_invert(1), 0xFFFFFFFF - 1);
    assert_eq!(fract32_invert(54321), 0xFFFFFFFF - 54321);
    assert_eq!(fract32_invert(0xFFFFFFF0), 0xFFFFFFFF - 0xFFFFFFF0);
}

#[cfg(not(feature = "fixmath_no_64bit"))]
#[test]
fn public_test_fract32_usmul() {
    assert_eq!(fract32_usmul(200, 0x40000000), 50);
    assert_eq!(fract32_usmul(654321, 0xFFFFFFFF), 654321);
    assert_eq!(fract32_usmul(6543, 0), 0);
}

#[cfg(not(feature = "fixmath_no_64bit"))]
#[test]
fn public_test_fract32_smul() {
    assert_eq!(fract32_smul(200, 0x40000000), 50);
    assert_eq!(fract32_smul(-200, 0x40000000), -50);
    assert_eq!(fract32_smul(0, 0x40000000), 0);
}