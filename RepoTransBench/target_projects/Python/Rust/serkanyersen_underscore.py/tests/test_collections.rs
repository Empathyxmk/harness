use serkanyersen_underscore::underscore::map_;

#[test]
fn test_map() {
    let input = vec![1, 2, 3];
    let result = map_(&input, |x| x * 2);
    assert_eq!(result, vec![2, 4, 6]);
}