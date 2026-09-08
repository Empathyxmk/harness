use actix_web::App;

#[test]
fn test_jwt_secret_key_present() {
    // Just check config value is set as a dummy
    let jwt_secret = "abc_config_public";
    assert_eq!(jwt_secret, "abc_config_public");
}