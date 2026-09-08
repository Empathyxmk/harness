use cloudconvert_cloudconvert_rust::environment_vars;

use std::env;

#[test]
fn test_read_api_key_env_var() {
    env::set_var("CLOUDCONVERT_API_KEY", "envkey123");
    let api_key = environment_vars::get_api_key_from_env();
    assert_eq!(api_key, Some("envkey123".to_string()));
    env::remove_var("CLOUDCONVERT_API_KEY");
}

#[test]
fn test_unset_api_key_env_var() {
    env::remove_var("CLOUDCONVERT_API_KEY");
    let api_key = environment_vars::get_api_key_from_env();
    assert_eq!(api_key, None);
}