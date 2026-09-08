use serkanyersen_underscore::underscore::{chunk, compact, Compactable};

#[test]
fn test_chunk() {
    let v = vec![1, 2, 3, 4];
    let expected = vec![vec![1, 2], vec![3, 4]];
    assert_eq!(chunk(&v, 2), expected);
}

#[test]
fn test_compact() {
    use Compactable::*;
    let arr = vec![Int(0), Int(1), Bool(false), Int(2), String("".into()), Int(3)];
    let expected = vec![Int(1), Int(2), Int(3)];
    assert_eq!(compact(&arr), expected);
}