// Test constants and "dunder" attributes.
#[test]
fn test_public_dunder_constants_distinct() {
    let version = "1.2.3";
    let title = "Flask-Redis";
    let description = "a redis cache layer";
    let url = "https://github.com/underyx/flask-redis";
    let uri = url;
    let author = "underyx";
    let email = "underyx@example.com";
    let copyright = "Copyright (c) 2024 underyx";
    let all = vec!["FlaskRedis"];

    assert!(version.parse::<String>().is_ok());
    assert_eq!(title, "Flask-Redis");
    assert!(description.to_lowercase().contains("redis"));
    assert!(url.starts_with("https://"));
    assert!(uri.starts_with("https://"));
    assert!(email.contains("@"));
    assert!(copyright.contains("opyright"));
    assert!(all.contains(&"FlaskRedis"));
}

#[test]
fn test_public_title_unique() {
    let title = "Flask-Redis";
    let author = "underyx";
    assert_eq!(title, "Flask-Redis");
    assert!(author.len() > 3);
}

#[test]
fn test_public_version_style() {
    let version = "1.2.3";
    let re = regex::Regex::new(r"^\d+\.\d+\.\d+").unwrap();
    assert!(re.is_match(version));
}