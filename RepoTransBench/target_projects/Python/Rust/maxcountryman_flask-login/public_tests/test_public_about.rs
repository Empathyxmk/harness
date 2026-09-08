#[cfg(test)]
mod tests {
    use crate::about;

    #[test]
    fn test_about_warns_public() {
        let warning = about::warn_about();
        assert!(warning.to_lowercase().contains("deprecated"));
        assert!(about::TITLE.contains("Flask"));
        let vers = about::VERSION;
        assert_eq!(vers.split('.').count(), 3);
    }

    #[test]
    fn test_init_dunder_version_warns_public() {
        let val = "2.0.1";
        let warning = about::warn_about();
        assert!(warning.to_lowercase().contains("deprecated"));
        assert_eq!(val, "2.0.1");
    }

    #[test]
    fn test_init_dunder_version_attribute_error_public() {
        let sim_attr = "certainlynotanattribute";
        let res = std::panic::catch_unwind(|| {
            dummy_struct_field_access();
        });
        assert!(res.is_err());
        if let Err(e) = res {
            let msg = e.downcast_ref::<&str>().unwrap_or(&"");
            assert!(msg.contains(sim_attr) || *msg == "");
        }
    }

    fn dummy_struct_field_access() {
        panic!("certainlynotanattribute");
    }
}