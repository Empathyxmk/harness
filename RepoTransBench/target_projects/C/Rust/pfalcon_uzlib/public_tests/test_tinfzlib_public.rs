// Test translated from tests/unit/test_tinfzlib_public.c

use pfalcon_uzlib::*;

#[test]
fn tinfzlib_public_header_parse() {
    // Test zlib header parse: valid public test with different CMF/FLG bytes than in original private test
    // Valid zlib header with CMF=0x28, FLG=0x51, (0x2851 % 31 == 0), CM=8 (deflate)
    let valid_header = [0x28u8, 0x51];
    let mut d = TINF_DATA::new(&valid_header);
    let res = uzlib_zlib_parse_header(&mut d);
    assert_eq!(res, TINF_OK);

    // Invalid CMF (CM != 8)
    let invalid_cmf = [0x24u8, 0x50];
    let mut d = TINF_DATA::new(&invalid_cmf);
    let res = uzlib_zlib_parse_header(&mut d);
    assert_eq!(res, TINF_DATA_ERROR);

    // Invalid FCHECK
    let invalid_fcheck = [0x28u8, 0x52];
    let mut d = TINF_DATA::new(&invalid_fcheck);
    let res = uzlib_zlib_parse_header(&mut d);
    assert_eq!(res, TINF_DATA_ERROR);
}