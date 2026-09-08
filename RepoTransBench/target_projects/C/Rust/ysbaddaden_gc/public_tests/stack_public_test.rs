use ysbaddaden_gc::stack::Stack;

#[test]
fn test_stack_ops_public() {
    let mut st: Stack<i32> = Stack::new();
    let mut values = vec![10,20,30,40,50];
    for v in &values {
        st.buffer.push(*v);
    }
    assert_eq!(st.buffer.len(), 5);
    assert_eq!(*st.buffer.last().unwrap(), 50);
    while let Some(v) = st.buffer.pop() {
        assert!(values.contains(&v));
    }
    assert_eq!(st.buffer.len(), 0);
}