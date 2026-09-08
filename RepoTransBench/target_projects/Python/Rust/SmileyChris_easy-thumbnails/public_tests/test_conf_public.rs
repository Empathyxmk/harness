// Translated from public_tests/test_conf_public.py

#[test]
fn test_default_settings_public() {
    struct EasyThumbSettings {
        thumbnails_basedir: &'static str,
    }
    let s = EasyThumbSettings { thumbnails_basedir: "thumbnails" };
    assert_eq!(s.thumbnails_basedir, "thumbnails");
}