use jpeg_quantsmooth::libjpegqs::JpegqsControl;

#[test]
fn test_jpegqs_control_default() {
    let opts = JpegqsControl::default();
    assert_eq!(opts.flags, 0);
    assert_eq!(opts.quality, 0);
    assert_eq!(opts.iter, 0);
}