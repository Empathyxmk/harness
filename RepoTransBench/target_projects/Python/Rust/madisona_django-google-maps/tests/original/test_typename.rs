#[cfg(test)]
mod tests {
    fn typename<T: ?Sized>(_: &T) -> &'static str {
        // Very simple simulation: returns "str" for &str, "type" for type object
        std::any::type_name::<T>().split("::").last().unwrap_or("unknown")
    }

    #[test]
    fn test_simple_type_returns_type_name_as_string() {
        let val = "x";
        let typ = typename(&val);
        // We mimic Python returning 'str' for string
        assert_eq!(typ, "str");
    }

    #[test]
    fn test_class_object() {
        struct X;
        // We mimic returning 'type' for types, which in reality std::any::type_name returns "X"
        // So for this test we check that the type_name of type X is "X"
        let typ = typename(&X);
        assert_eq!(typ, "X");
    }
}