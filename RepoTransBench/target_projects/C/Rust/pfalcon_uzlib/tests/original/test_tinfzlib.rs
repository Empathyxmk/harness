// Tests translated from tests/unit/test_tinfzlib.c

use pfalcon_uzlib::*;

#[test]
fn test_zlib_parse_header_valid_and_invalid() {
    // Use a static mutable dummy_buf for input
    let mut dummy_buf = [0u8; 512];
    let mut d = TINF_DATA::new(&dummy_buf[0..2]);

    // Valid header: 0x78 0x9C
    dummy_buf[0] = 0x78; dummy_buf[1] = 0x9C;
    let mut d1 = TINF_DATA::new(&dummy_buf[0..2]);
    let res = uzlib_zlib_parse_header(&mut d1);
    assert_eq!(res, 7);
    assert_eq!(d1.checksum_type, TINF_CHKSUM_ADLER);
    assert_eq!(d1.checksum, 1);

    // Invalid FLG: 0x78 0x9D
    dummy_buf[0] = 0x78; dummy_buf[1] = 0x9D;
    let mut d2 = TINF_DATA::new(&dummy_buf[0..2]);
    let res = uzlib_zlib_parse_header(&mut d2);
    assert_eq!(res, TINF_DATA_ERROR);

    // Invalid CMF: 0x71 0x9B
    dummy_buf[0] = 0x71; dummy_buf[1] = 0x9B;
    let mut d3 = TINF_DATA::new(&dummy_buf[0..2]);
    let res = uzlib_zlib_parse_header(&mut d3);
    assert_eq!(res, TINF_DATA_ERROR);

    // Another invalid header: 0xF8 0xCD
    dummy_buf[0] = 0xF8; dummy_buf[1] = 0xCD;
    let mut d4 = TINF_DATA::new(&dummy_buf[0..2]);
    let res = uzlib_zlib_parse_header(&mut d4);
    assert_eq!(res, TINF_DATA_ERROR);

    // FDICT bit set: 0x78 (CMF), 0xBC | 0x20, then 0x9C | 0x20
    dummy_buf[0] = 0x78; dummy_buf[1] = 0x9C | 0x20;
    let mut d5 = TINF_DATA::new(&dummy_buf[0..2]);
    let res = uzlib_zlib_parse_header(&mut d5);
    assert_eq!(res, TINF_DATA_ERROR);
}