use bagder_spindly::{
    SpdyFrame, SpdyData, SPDY_ERROR_NONE, SPDY_CONTROL_FRAME, SPDY_DATA_FRAME,
    spdy_frame_init, spdy_frame_parse_header
};

#[test]
fn test_spdy_frame_init() {
    let mut frame = SpdyFrame::default();
    let rc = spdy_frame_init(&mut frame);
    assert_eq!(rc, SPDY_ERROR_NONE);
    assert!(frame.prev.is_none());
    assert!(frame.next.is_none());
    assert_eq!(frame._header_parsed, 0);
}

#[test]
fn test_spdy_frame_parse_header_control() {
    let mut frame = SpdyFrame::default();
    let buf: [u8; 1] = [0x80];
    let data = SpdyData { cursor: buf.as_ptr() };
    
    let rc = spdy_frame_parse_header(&mut frame, &data);
    assert_eq!(rc, SPDY_ERROR_NONE);
    assert_eq!(frame.type_, SPDY_CONTROL_FRAME);
}

#[test]
fn test_spdy_frame_parse_header_data() {
    let mut frame = SpdyFrame::default();
    let buf: [u8; 1] = [0x00];
    let data = SpdyData { cursor: buf.as_ptr() };
    
    let rc = spdy_frame_parse_header(&mut frame, &data);
    assert_eq!(rc, SPDY_ERROR_NONE);
    assert_eq!(frame.type_, SPDY_DATA_FRAME);
}