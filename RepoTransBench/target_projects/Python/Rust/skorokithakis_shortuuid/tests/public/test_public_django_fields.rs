#[cfg(test)]
mod tests {
    #[test]
    fn test_public_django_field_import() {
        super::super::original::test_django_fields::tests::test_django_field_import();
    }
    #[test]
    fn test_public_django_field_str_and_repr() {
        super::super::original::test_django_fields::tests::test_django_field_str_and_repr();
    }
}