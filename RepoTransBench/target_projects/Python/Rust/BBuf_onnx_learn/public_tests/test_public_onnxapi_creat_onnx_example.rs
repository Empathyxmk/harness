use bbuf_onnx_learn::onnxapi::creat_onnx_example::{make_identity, sum_list};

#[test]
fn test_make_identity() {
    assert_eq!(make_identity(String::from("hello")), String::from("hello"));
    assert_eq!(make_identity(vec![7, 8, 9]), vec![7, 8, 9]);
}

#[test]
fn test_sum_list() {
    assert_eq!(sum_list(&[4, 5, 6]), 15);
    assert_eq!(sum_list(&[100]), 100);
}