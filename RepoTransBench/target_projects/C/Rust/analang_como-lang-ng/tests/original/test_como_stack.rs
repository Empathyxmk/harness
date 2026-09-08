use analang_como_lang_ng::stack::ComoStack;

#[test]
fn test_stack_push_and_pop() {
    let mut s = ComoStack::new();
    s.push(10i32);
    assert_eq!(s.top::<i32>(), Some(&10));
    let v: Option<i32> = s.pop();
    assert_eq!(v, Some(10));
    // Pop from empty stack
    let v2: Option<i32> = s.pop();
    assert_eq!(v2, None);
}

#[test]
fn test_stack_clear() {
    let mut s = ComoStack::new();
    s.push(1i32);
    s.push(2i32);
    s.clear();
    assert_eq!(s.size(), 0);
}