#[test]
fn test_dummy_server_start() {
    // As in python test, assert that we can use HammsServer struct
    let _ = kevinburke_hamms::HammsServer::new();
    assert!(true);
}