use haishoku_rs::alg;
use std::collections::HashMap;

#[test]
fn test_rgb2hls_variation() {
    assert_eq!(alg::rgb2hls((200, 150, 100)), (30, 150, 102));
}

#[test]
fn test_get_histogram_variation() {
    let result = alg::get_histogram(vec![(100,100,100), (100,100,100), (50,50,50)]);
    let mut expected = HashMap::new();
    expected.insert((100,100,100), 2);
    expected.insert((50,50,50), 1);
    assert_eq!(result, expected);
}