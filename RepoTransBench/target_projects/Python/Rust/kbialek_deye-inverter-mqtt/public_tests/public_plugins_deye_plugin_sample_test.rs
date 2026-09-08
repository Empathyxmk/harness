// Public: Translated from public_tests/public_plugins_deye_plugin_sample_test.py

#[test]
fn test_plugin_pub_name() {
    let plug = PubPluginSample::new("hello");
    assert_eq!(plug.name(), "hello");
}

struct PubPluginSample { nm: String }
impl PubPluginSample {
    fn new(n: &str) -> Self { Self { nm: n.to_string() } }
    fn name(&self) -> &str { &self.nm }
}