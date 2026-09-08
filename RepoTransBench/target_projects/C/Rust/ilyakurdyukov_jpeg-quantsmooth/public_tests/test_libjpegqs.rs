use std::mem;
use jpeg_quantsmooth::libjpegqs::JpegqsControl;

#[test]
fn test_jpegqs_control_nondefault() {
    let mut opts = JpegqsControl::default();
    opts.flags = 1;
    opts.quality = 85;
    opts.iter = 2;
    
    assert_eq!(opts.flags, 1);
    assert_eq!(opts.quality, 85);
    assert_eq!(opts.iter, 2);
}

#[test]
fn test_jpegqs_control_reset() {
    // Initialize with non-zero values
    let mut opts = JpegqsControl {
        flags: 0xAA,
        quality: 0xAA,
        iter: 0xAA,
    };
    
    // Reset to default zero
    opts = JpegqsControl::default();
    
    assert_eq!(opts.flags, 0);
    assert_eq!(opts.quality, 0);
    assert_eq!(opts.iter, 0);
}