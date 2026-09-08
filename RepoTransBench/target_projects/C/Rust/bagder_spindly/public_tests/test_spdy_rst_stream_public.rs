use bagder_spindly::fake_rst_stream_error;

#[test]
fn test_fake_rst_stream_error_values() {
    assert_eq!(fake_rst_stream_error(6), -106);
    assert_eq!(fake_rst_stream_error(17), -117);
    assert_eq!(fake_rst_stream_error(88), 1);
}