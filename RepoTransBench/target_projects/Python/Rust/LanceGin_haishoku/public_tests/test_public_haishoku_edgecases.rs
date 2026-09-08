use haishoku_rs::alg;

#[test]
fn test_rgb2hls_boundary() {
    assert_eq!(alg::rgb2hls((0, 0, 0)), (0, 0, 0));
    assert_eq!(alg::rgb2hls((255, 255, 255)), (0, 255, 0));
}