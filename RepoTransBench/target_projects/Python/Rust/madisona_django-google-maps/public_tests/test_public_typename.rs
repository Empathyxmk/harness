#[cfg(test)]
mod public_typename {
    fn typename<T: ?Sized>(_: &T) -> &'static str {
        std::any::type_name::<T>().split("::").last().unwrap_or("unknown")
    }

    #[test]
    fn test_simple_type_returns_type_name_as_string_public() {
        let val = "abc";
        let typ = typename(&val);
        assert_eq!(typ, "str");
    }

    #[test]
    fn test_class_object_public() {
        struct Y;
        let typ = typename(&Y);
        assert_eq!(typ, "Y");
    }
}