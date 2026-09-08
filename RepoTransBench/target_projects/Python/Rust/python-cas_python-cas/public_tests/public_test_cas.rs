#[test]
fn test_public_login_url() {
    let client = cas::CASClientBase {
        renew: true,
        extra_login_params: None,
        server_url: "https://cas.logouttest.org/auth/".to_owned(),
        service_url: "http://mydomain/hello".to_owned(),
    };

    assert_eq!(
        client.get_login_url(),
        "https://cas.logouttest.org/auth/login?service=https%3A%2F%2Fmydomain%2Fhello%2F"
    )
}