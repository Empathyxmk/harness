mod cas;

#[test]
fn test_login_url_helper() {
    let client = cas::CASClientBase {
        renew: false,
        extra_login_params: None,
        server_url: "http://www.example.com/cas/".to_string(),
        service_url: "http://testserver/".to_string(),
    };
    let actual = client.get_login_url();
    let expected = "http://www.example.com/cas/login?service=http%3A%2F%2Ftestserver%2F";
    assert_eq!(actual, expected);
}

#[test]
fn test_login_url_helper_with_extra_params() {
    use std::collections::HashMap;

    let mut params = HashMap::new();
    params.insert("test".to_string(), "1234".to_string());

    let client = cas::CASClientBase {
        renew: false,
        extra_login_params: Some(params),
        server_url: "http://www.example.com/cas/".to_string(),
        service_url: "http://testserver/".to_string(),
    };

    let actual = client.get_login_url();
    assert!(actual.contains("service=http%3A%2F%2Ftestserver%2F"));
    assert!(actual.contains("test=1234"));
}

#[test]
fn test_login_url_helper_with_renew() {
    let client = cas::CASClientBase {
        renew: true,
        extra_login_params: None,
        server_url: "http://www.example.com/cas/".to_string(),
        service_url: "http://testserver/".to_string(),
    };
    let actual = client.get_login_url();
    assert!(actual.contains("service=http%3A%2F%2Ftestserver%2F"));
    assert!(actual.contains("renew=true"));
}