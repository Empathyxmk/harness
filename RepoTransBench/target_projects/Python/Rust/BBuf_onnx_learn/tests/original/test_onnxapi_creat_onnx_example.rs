use bbuf_onnx_learn::onnxapi::creat_onnx_example::{make_identity, sum_list};

#[test]
fn test_make_identity() {
    assert_eq!(make_identity(100), 100);
    assert_eq!(make_identity(vec![1, 2, 3]), vec![1, 2, 3]);
}

#[test]
fn test_sum_list() {
    assert_eq!(sum_list(&[1, 2, 3]), 6);
    assert_eq!(sum_list::<i32>(&[]), 0);
}