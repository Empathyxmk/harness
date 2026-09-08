use bagder_spindly::{
    SpdyNvBlock, SpdyHeaders, SpindlyPhys,
    spdy_headers_parse_header
};

#[test]
fn test_spdy_headers_parse_header_success_fn() {
    let mut block = SpdyNvBlock::default();
    let mut headers = SpdyHeaders::default();
    headers.nv_block = &mut block;
    let phys = SpindlyPhys::default();
    
    let rc = spdy_headers_parse_header(Some(&mut headers), Some(&phys));
    assert_eq!(rc, 0);
}

#[test]
fn test_spdy_headers_parse_header_null_ptr() {
    let rc = spdy_headers_parse_header(None, None);
    assert_eq!(rc, -1);
}