use ysbaddaden_gc::stack::Stack;

#[test]
fn test_stack_init() {
    let stack: Stack<i32> = Stack::new();
    assert_eq!(stack.buffer.len(), 0);
    assert!(stack.buffer.is_empty());
}