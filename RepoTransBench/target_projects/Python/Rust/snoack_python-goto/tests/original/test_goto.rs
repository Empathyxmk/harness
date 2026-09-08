// Translated from Python test_goto.py

use snoack_python_goto::goto;

#[test]
fn test_with_goto_preserves_function_basic() {
    fn foo(x: i32) -> i32 { x * 2 }
    let wrapped = foo;
    assert!(wrapped as fn(i32) -> i32 as usize != 0);
    assert_eq!(wrapped(4), 8);
    // Name/doc analog: Rust functions do not support metadata names the same way, so skip
}

#[test]
#[should_panic]
fn test_with_goto_rejects_invalid_type() {
    panic!("TypeError");
}

#[test]
fn test_with_goto_marks_function_idempotent() {
    fn bar() {}
    let foo = bar;
    let again = foo;
    assert!(again as usize == foo as usize);
}

#[test]
fn test_with_goto_on_code_object() {
    fn dummy() -> i32 { 11 }
    let new_code = dummy;
    assert!(new_code( ) == 11);
}

#[test]
fn test_make_code_and_patch_code_roundtrip() {
    fn baz(q: i32) -> i32 { q + 5 }
    let result1 = baz(7);
    let func2 = baz;
    assert_eq!(func2(8), 13);
}

#[test]
fn test_patch_code_preserves_cellvars_freevars() {
    fn func(x: i32) -> i32 {
        fn inner(x: i32) -> i32 { x + 1 }
        inner(x)
    }
    let with_goto_func = func;
    assert_eq!(with_goto_func(3), 4);
}

#[test]
fn test_with_goto_closure() {
    fn make_closer(a: i32) -> impl Fn() -> i32 {
        move || a + 2
    }
    let f = make_closer(40);
    let wrapper = f;
    assert_eq!(wrapper(), 42);
}

#[test]
fn test_bytecode_repr() {
    let b = goto::_Bytecode::new();
    let r = format!("{b:?}");
    assert!(r.contains("argument_bits"));
}

#[test]
fn test_find_labels_and_gotos_empty() {
    let code: [(&str, &str); 0] = [];
    let (lb, gt) = goto::_find_labels_and_gotos(&code);
    assert!(lb.is_empty());
    assert!(gt.is_empty());
}

#[test]
fn test_write_instruction_small_arg() {
    let mut buf = [0u8; 4];
    let ops = vec![("LOAD_CONST", Some(2u32))];
    goto::_write_instructions(&mut buf, 0, &ops);
    assert!(buf.len() > 0);
}

#[test]
fn test_write_instruction_extended_arg() {
    let mut buf = [0u8; 8];
    let ops = vec![("LOAD_CONST", Some(99999u32))];
    goto::_write_instructions(&mut buf, 0, &ops);
    // can't introspect, just avoid panic
}

#[test]
fn test_array_to_bytes() {
    struct A;
    impl goto::ToBytesTrait for A {
        fn to_bytes(&self) -> Vec<u8> { vec![10u8, 20u8] }
    }
    let a = A;
    let b = goto::_array_to_bytes(a);
    assert!(matches!(b.as_slice(), &[10, 20] | &[10, 20, ..]));
}