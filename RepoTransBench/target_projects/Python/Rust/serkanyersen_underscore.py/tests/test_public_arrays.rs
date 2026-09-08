// This is a PUBLIC test file.
use serkanyersen_underscore::underscore::{chunk, compact, Compactable};

#[test]
fn test_chunk_public() {
    let v = vec![10, 20, 30, 40, 50];
    let expected = vec![vec![10, 20, 30], vec![40, 50]];
    assert_eq!(chunk(&v, 3), expected);
}

#[test]
fn test_compact_public() {
    use Compactable::*;
    let arr = vec![
        None, String("hello".into()), String("".into()), Int(0), Int(9), Bool(false), Int(5)
    ];
    let expected = vec![
        String("hello".into()), Int(9), Int(5)
    ];
    assert_eq!(compact(&arr), expected);
}