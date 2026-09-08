#[test]
fn test_import_reloadable() {
    use std::collections::HashMap;

    let client = cas::CASClientBase {
        renew: false,
        extra_login_params: HashMap::new(),
        server_url: "http://smoke.cas.org/server/".to_owned(),
        service_url: "http://smoke.cas.org/client/".to_owned(),
    };

    let actual = client.get_logout_url(Some("http://example.com/small".to_string()));
    assert!(actual.contains("small"));
}