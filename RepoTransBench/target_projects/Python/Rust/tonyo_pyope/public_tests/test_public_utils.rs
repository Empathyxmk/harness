#[test]
fn test_chunks_manual_public() {
    let lst = vec![11, 22, 33, 44, 55, 66, 77, 88];
    let n = 2;
    let mut result: Vec<Vec<i32>> = vec![];
    let mut i = 0;
    while i < lst.len() {
        let end = std::cmp::min(i + n, lst.len());
        result.push(lst[i..end].to_vec());
        i += n;
    }
    assert_eq!(result, vec![vec![11, 22], vec![33,44], vec![55,66], vec![77,88]]);
}