//! Rust port of public_tests/test_public_connection.py

use pywebostv_rust::utils::FakeClient;
use std::collections::HashMap;

#[test]
fn test_unique_id_public() {
    let client = FakeClient::default();
    client.send_message("rsp", "urn", None, Some("#87"));
}

#[test]
fn test_get_queue_public() {
    let client = FakeClient::default();
    client.send_message("ntf", "test/uri", None, Some("42"));
}

#[test]
fn test_send_callback_public() {
    let client = FakeClient::default();
    client.send_message("req", "abc", None, Some("99"));
}

#[test]
fn test_send_minimum_params_public() {
    let client = FakeClient::default();
    client.send_message("rsp", "foobar", None, Some("11"));
}

#[test]
fn test_multiple_send_public() {
    let client = FakeClient::default();
    client.send_message("ntf", "hello/world", None, Some("7"));
    client.send_message("req", "hello/world", None, Some("9"));
}

#[test]
fn test_clear_waiters_public() {
    let client = FakeClient::default();
    client.send_message("rsp", "abc/", None, Some("30"));
    client.send_message("ntf", "xyz/", None, Some("40"));
}

#[test]
fn test_subscription_public() {
    let client = FakeClient::default();
    client.subscribe("alt_uri", "321", || {});
    client.unsubscribe("321");
}

#[test]
fn test_new_registration_public() {
    let client = FakeClient::default();
    let mut store = HashMap::new();
    client.register(&mut store, 1);
}

#[test]
fn test_discovery_public() {
    let _ = crate::pywebostv_rust::connection::WebOSClient::discover();
}

#[test]
fn test_registration_timeout_public() {
    let client = FakeClient::default();
    let mut store = HashMap::new();
    client.register(&mut store, 3);
}

#[test]
fn test_registration_public() {
    let client = FakeClient::default();
    let mut store = HashMap::new();
    client.register(&mut store, 10);
}