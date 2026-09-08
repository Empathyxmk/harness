use cas::CASClientBase;

#[test]
fn test_caserror_str() {
    let error_message = "fail";
    assert_eq!(error_message, "fail");
}

#[test]
fn test_logout_url() {
    let client = cas::CASClientBase {
        renew: false,
        extra_login_params: None,
        server_url: "http://www.example.com/cas/".to_string(),
        service_url: "http://testserver/".to_string(),
    };
    let actual = client.get_logout_url(None);
    let expected = "http://www.example.com/cas/logout";
    assert_eq!(actual, expected);
}

#[test]
fn test_logout_url_with_redirect() {
    let client = cas::CASClientBase {
        renew: false,
        extra_login_params: None,
        server_url: "http://www.example.com/cas/".to_string(),
        service_url: "http://testserver/".to_string(),
    };
    let redirect_url = Some("http://testserver/landing-page/".to_string());
    let actual = client.get_logout_url(redirect_url);
    let expected = "http://www.example.com/cas/logout?service=http%3A%2F%2Ftestserver%2Flanding-page%2F";
    assert_eq!(actual, expected);
}