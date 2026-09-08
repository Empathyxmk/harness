use cloudconvert_cloudconvert_rust::environment_vars;

#[test]
fn test_public_api_key_env_none() {
    std::env::remove_var("CLOUDCONVERT_API_KEY");
    let val = environment_vars::get_api_key_from_env();
    assert_eq!(val, None);
}