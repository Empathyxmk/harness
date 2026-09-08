use underyx_flask_redis::{
    __VERSION__, __TITLE__, __DESCRIPTION__, __URL__, __URI__, __AUTHOR__, __EMAIL__,
    __LICENSE__, __COPYRIGHT__, __ALL__, FlaskRedis
};

#[test]
fn test_metadata_constants() {
    assert!(!__VERSION__.is_empty());
    assert_eq!(__TITLE__, "flask-redis");
    assert!(!__DESCRIPTION__.is_empty());
    assert!(__URL__.starts_with("https://"));
    assert_eq!(__URI__, __URL__);
    assert!(!__AUTHOR__.is_empty());
    assert!(__EMAIL__.contains("@"));
    assert!(!__LICENSE__.is_empty());
    assert!(__COPYRIGHT__.contains("Copyright"));
}

#[test]
fn test_all_list() {
    // Simulate Python "FlaskRedis in __all__"
    assert_eq!(__ALL__[0], "FlaskRedis");
}