use pywizlight_rust::utils;

#[tokio::test]
async fn test_generate_mac() {
    assert_eq!(utils::generate_mac().len(), 12);
}

#[tokio::test]
async fn test_get_source_ip() {
    assert_eq!(utils::get_source_ip("127.0.0.1"), "127.0.0.1");
}