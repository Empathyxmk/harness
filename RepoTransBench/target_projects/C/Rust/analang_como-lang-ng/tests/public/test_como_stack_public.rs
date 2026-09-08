use analang_como_lang_ng::stack::ComoStack;

#[test]
fn test_stack_push_pop_public() {
    let mut stack = ComoStack::new();
    let value = 987654i32;
    stack.push(value);
    let ret: Option<i32> = stack.pop();
    assert_eq!(ret, Some(987654));
}

#[test]
fn test_stack_push2_public() {
    let mut stack = ComoStack::new();
    let a = -1i32;
    let b = 0i32;
    stack.push(a);
    stack.push(b);
    let retb: Option<i32> = stack.pop();
    let reta: Option<i32> = stack.pop();
    assert_eq!(retb, Some(0));
    assert_eq!(reta, Some(-1));
}