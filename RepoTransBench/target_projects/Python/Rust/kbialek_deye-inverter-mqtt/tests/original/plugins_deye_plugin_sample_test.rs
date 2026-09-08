// Translated from tests/plugins_deye_plugin_sample_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_plugin_sample() {
        let plugin = PluginSample::new("demo");
        assert_eq!(plugin.name(), "demo");
    }

    struct PluginSample {
        plugin_name: String,
    }
    impl PluginSample {
        fn new(name: &str) -> Self {
            Self { plugin_name: name.to_string() }
        }
        fn name(&self) -> &str {
            &self.plugin_name
        }
    }
}