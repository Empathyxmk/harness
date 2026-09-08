use python3_oop_rust::echo_server::{EchoServer, EchoClient};

#[test]
fn test_echo() {
    let server = EchoServer;
    let client = EchoClient::new(&server);
    let msg = "hello";
    let response = client.send(msg);
    assert_eq!(response, msg);
}

#[test]
fn test_echo_empty() {
    let server = EchoServer;
    let client = EchoClient::new(&server);
    let msg = "";
    let response = client.send(msg);
    assert_eq!(response, "");
}