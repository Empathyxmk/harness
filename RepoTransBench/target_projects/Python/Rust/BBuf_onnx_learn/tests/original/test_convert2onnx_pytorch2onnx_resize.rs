use bbuf_onnx_learn::convert2onnx::pytorch2onnx_resize::dummy_resize_func;

#[test]
fn test_dummy_resize_func() {
    assert_eq!(dummy_resize_func(4, 5), (4, 5));
    assert_eq!(dummy_resize_func("x", 42), ("x", 42));
}