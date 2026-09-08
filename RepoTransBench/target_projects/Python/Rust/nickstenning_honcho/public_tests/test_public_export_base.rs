use crate::export::base::Exporter;

#[test]
fn test_exporter_env_public() {
    let e = Exporter;
    let env = e.read_environment("some/path/to/envfile");
    assert_eq!(env["HELLO"], "world");
    assert_eq!(env["PUBLIC"], "success");
}