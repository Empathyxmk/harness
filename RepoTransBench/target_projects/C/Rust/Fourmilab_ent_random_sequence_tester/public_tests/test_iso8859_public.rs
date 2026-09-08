use fourmilab_ent_random_sequence_tester::iso8859::*;

#[test]
fn test_is_iso_alpha_public() {
    assert!(is_iso_alpha(b'B'));
    assert!(is_iso_alpha(b'y'));
    assert!(!is_iso_alpha(b'2'));
    assert!(!is_iso_alpha(b'@'));
    assert!(is_iso_alpha(0xC4));
    assert!(is_iso_alpha(0xE4));
}

#[test]
fn test_is_iso_upper_public() {
    assert!(is_iso_upper(b'Z'));
    assert!(!is_iso_upper(b'z'));
    assert!(is_iso_upper(0xD1));
}

#[test]
fn test_is_iso_lower_public() {
    assert!(is_iso_lower(b'm'));
    assert!(!is_iso_lower(b'M'));
    assert!(is_iso_lower(0xF1));
}

#[test]
fn test_is_iso_space_public() {
    assert!(is_iso_space(b'\t'));
    assert!(!is_iso_space(b'B'));
    assert!(is_iso_space(0x0A));
}

#[test]
fn test_is_iso_print_public() {
    assert!(is_iso_print(b'$'));
    assert!(is_iso_print(b'q'));
    assert!(is_iso_print(0xB0));
    assert!(!is_iso_print(b'\r'));
    assert!(!is_iso_print(b'\x0B'));
}