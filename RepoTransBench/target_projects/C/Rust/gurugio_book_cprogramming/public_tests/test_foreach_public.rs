use gurugio::macro_if_foreach;

#[test]
fn test_macro_if_foreach_success_public() {
    let ret = macro_if_foreach('c');
    assert_eq!(ret, 3);
    
    let ret = macro_if_foreach('d');
    assert_eq!(ret, 4);
    
    let ret = macro_if_foreach('e');
    assert_eq!(ret, 5);
    
    let ret = macro_if_foreach('a');
    assert_eq!(ret, 1);
    
    let ret = macro_if_foreach('b');
    assert_eq!(ret, 2);
}

#[test]
fn test_macro_if_foreach_invalid_public() {
    let ret = macro_if_foreach('y');
    assert_eq!(ret, -1);
    
    let ret = macro_if_foreach('%');
    assert_eq!(ret, -1);
}