// This is a PUBLIC test file.
use serkanyersen_underscore::underscore::map_;

#[test]
fn test_map_public() {
    let input = vec![4, 5, 6];
    let output = map_(&input, |x| x + 1);
    assert_eq!(output, vec![5, 6, 7]);
}