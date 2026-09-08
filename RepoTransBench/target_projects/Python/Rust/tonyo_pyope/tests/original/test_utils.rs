use crate::util::str_to_bitstring;

#[test]
fn test_bit_string_conversion() {
    assert_eq!(str_to_bitstring(b""), vec![]);
    assert_eq!(str_to_bitstring(b"A"), vec![0,1,0,0,0,0,0,1]);
    assert_eq!(str_to_bitstring(b"AB"), vec![0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,0]);
}