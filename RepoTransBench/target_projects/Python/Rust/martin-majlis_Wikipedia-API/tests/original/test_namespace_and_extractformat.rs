#[cfg(test)]
mod test_namespace_and_extractformat {
    use wikipediaapi::{Namespace, ExtractFormat, namespace2int};  // Assuming these are defined

    #[test]
    fn test_namespace_enum_members() {
        assert_eq!(Namespace::MAIN as u32, 0);
        assert_eq!(Namespace::USER as u32, 2);
        assert_eq!(Namespace::CATEGORY as u32, 14);
        assert_eq!(Namespace::BOOK as u32, 108);
        assert_eq!(Namespace::GADGET as u32, 2300);
    }

    #[test]
    fn test_extractformat_enum_members() {
        assert_eq!(ExtractFormat::WIKI as u32, 1);
        assert_eq!(ExtractFormat::HTML as u32, 2);
    }

    #[test]
    fn test_namespace2int_with_enum() {
        assert_eq!(namespace2int(Namespace::MAIN), 0);
        assert_eq!(namespace2int(Namespace::CATEGORY), 14);
    }

    #[test]
    fn test_namespace2int_with_int() {
        assert_eq!(namespace2int(42), 42);
        assert_eq!(namespace2int(0), 0);
    }

    #[test]
    fn test_invalid_namespace2int() {
        assert_eq!(namespace2int(Namespace::USER_TALK), Namespace::USER_TALK as u32);  // Assuming it returns the value
    }

    #[test]
    fn test_extractformat_repr() {
        assert_eq!(ExtractFormat::WIKI.to_string(), "WIKI");
        assert_eq!(ExtractFormat::HTML.to_string(), "HTML");
    }
}