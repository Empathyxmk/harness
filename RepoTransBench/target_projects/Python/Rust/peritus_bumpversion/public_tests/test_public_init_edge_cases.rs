use peritus_bumpversion::bump_mod::ConfiguredFile;
use std::collections::HashMap;

#[test]
fn test_config_file_section_defaults() {
    let mut conf = HashMap::new();
    conf.insert("current_version", "2.2.2");
    conf.insert("parse", "abc(?P<alpha>[a-zA-Z]+)");
    conf.insert("serialize", "{alpha}");
    let options = ConfiguredFile::new("setup.cfg", &conf);
    assert_eq!(options.serialize, vec!["{alpha}".to_string()]);
}

#[test]
fn test_default_parse_pattern_is_used_new() {
    let mut conf = HashMap::new();
    conf.insert("current_version", "1.9.9");
    let options = ConfiguredFile::new("pyproject.toml", &conf);
    assert_eq!(options.config_file, "pyproject.toml".to_string());
}