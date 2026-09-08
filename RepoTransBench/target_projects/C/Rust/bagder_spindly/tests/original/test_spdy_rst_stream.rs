use bagder_spindly::{
    SpdyRstStream, SPDY_ERROR_NONE, SPDY_ERROR_INSUFFICIENT_DATA,
    spdy_rst_stream_parse
};

#[test]
fn test_spdy_rst_stream_parse_success() {
    let mut rst = SpdyRstStream::default();
    let data: [u8; 8] = [0, 0, 0, 0x10, 0, 0, 0, 1];
    
    let rc = spdy_rst_stream_parse(&mut rst, &data, 8);
    assert_eq!(rc, SPDY_ERROR_NONE);
    assert_eq!(rst.stream_id, 0x10);
    assert_eq!(rst.status_code, 0x01);
}

#[test]
fn test_spdy_rst_stream_parse_fail() {
    let mut rst = SpdyRstStream::default();
    let data: [u8; 4] = [0, 0, 0, 1];
    
    let rc = spdy_rst_stream_parse(&mut rst, &data, 4);
    assert_eq!(rc, SPDY_ERROR_INSUFFICIENT_DATA);
}