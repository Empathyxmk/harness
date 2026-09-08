use fourmilab_ent_random_sequence_tester::iso8859::*;

#[test]
fn test_is_iso_alpha() {
    assert!(is_iso_alpha(b'A'));
    assert!(is_iso_alpha(b'z'));
    assert!(!is_iso_alpha(b'1'));
    assert!(!is_iso_alpha(b'!'));
    assert!(is_iso_alpha(0xC1)); // Latin-1 upper
    assert!(is_iso_alpha(0xDF)); // Latin-1 lower (ß)
}

#[test]
fn test_is_iso_upper() {
    assert!(is_iso_upper(b'A'));
    assert!(!is_iso_upper(b'a'));
    assert!(is_iso_upper(0xC1));
}

#[test]
fn test_is_iso_lower() {
    assert!(is_iso_lower(b'a'));
    assert!(!is_iso_lower(b'A'));
    assert!(is_iso_lower(0xDF));
}

#[test]
fn test_is_iso_space() {
    assert!(is_iso_space(b' '));
    assert!(!is_iso_space(b'A'));
    assert!(is_iso_space(0xA0));
}

#[test]
fn test_is_iso_print() {
    assert!(is_iso_print(b'!'));
    assert!(is_iso_print(b'Z'));
    assert!(is_iso_print(0xA0));
    assert!(!is_iso_print(b'\n'));
    assert!(!is_iso_print(b'\t'));
}

#[test]
fn test_to_iso_upper() {
    assert_eq!(to_iso_upper(b'a'), b'A');
    assert_eq!(to_iso_upper(b'A'), b'A');
    assert_eq!(to_iso_upper(0xE1), 0xC1);
}

#[test]
fn test_to_iso_lower() {
    assert_eq!(to_iso_lower(b'A'), b'a');
    assert_eq!(to_iso_lower(b'a'), b'a');
    assert_eq!(to_iso_lower(0xC1), 0xE1);
}