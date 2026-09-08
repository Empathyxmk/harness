// Public client API tests in rust

#[test]
fn test_client_title_new_case() {
    let title = zaproxy_zap_api_rust::zapv2::core::title();
    assert!(title.len() > 3);
}

#[test]
fn test_client_banner_new_case() {
    let banner = zaproxy_zap_api_rust::zapv2::core::banner();
    assert!(banner.contains("ZAP") || banner.contains("Proxy"));
}