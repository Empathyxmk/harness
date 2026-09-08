#[cfg(test)]
mod tests {
    struct CustomResource {
        name: String,
        status: String,
    }
    impl CustomResource {
        fn new(name: &str) -> Self {
            CustomResource { name: name.to_string(), status: "new".to_string() }
        }
        fn use_resource(&mut self) {
            self.status = format!("{} used", self.name);
        }
        fn destroy(&mut self) {
            self.status = "destroyed".to_string();
        }
    }
    #[test]
    fn test_resource_name() {
        let mut res = CustomResource::new("RESOURCE_X_PUBLIC");
        assert_eq!(res.name, "RESOURCE_X_PUBLIC");
        res.use_resource();
        assert_eq!(res.status, "RESOURCE_X_PUBLIC used");
    }
    #[test]
    fn test_resource_destroy() {
        let mut res = CustomResource::new("RESOURCE_X_PUBLIC");
        res.destroy();
        assert_eq!(res.status, "destroyed");
    }
}