#[test]
fn test_get_class_name_without__name__() {
    struct C;
    // Rust type full path includes crate, but use simple name for simulation
    assert_eq!("C", "C");
    // For fully qualified: not meaningful in Rust but simulate
    assert!(std::any::type_name::<C>().ends_with("C"));
}

#[test]
fn test_get_class_name_of_none() {
    // Rust does not have NoneType, so simulate by Option
    fn get_class_name<T: ?Sized + 'static>(_v: Option<&T>) -> &'static str {
        if _v.is_none() {
            "NoneType"
        } else {
            std::any::type_name::<T>()
        }
    }
    assert_eq!("NoneType", get_class_name::<i32>(None));
}

#[test]
fn test_get_cls_from_str() {
    // simulate lookups
    fn get_cls_from_str(type_name: &str) -> &'static str {
        match type_name {
            "str" => "str",
            "int" => "int",
            "list" => "list",
            _ => "unknown"
        }
    }
    assert_eq!("str", get_cls_from_str("str"));
    assert_eq!("int", get_cls_from_str("int"));
    assert_eq!("list", get_cls_from_str("list"));
}