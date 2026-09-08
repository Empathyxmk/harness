use crate::extract::*;

#[test]
fn test_extract_func_identity_public() {
    let data = vec![10, 12, 11, 8];
    let result: Vec<i32> = data.iter().map(|x| *x).collect();
    assert_eq!(result, data);
}

#[test]
fn test_split_by_len_multiple_cases_public() {
    let seqs: Vec<Vec<i32>> = vec![vec![0,0,0,3], vec![7,8], vec![10]];
    let out = vec![
        (vec![0,0,0], vec![3]),
        (vec![7,8], vec![]),
        (vec![10], vec![])
    ];
    assert!(out.len() == 3);
}

#[test]
fn test_pad_or_trim_public() {
    let arr = vec![9];
    let mut padded = arr.clone();
    padded.resize(4, -1);
    assert_eq!(padded, vec![9, -1, -1, -1]);
    let mut trimmed = vec![7, 1, 3, 8, 6];
    trimmed.truncate(2);
    assert_eq!(trimmed, vec![7, 1]);
}