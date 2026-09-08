use medium_sdk_rust::Client;
use std::collections::HashMap;

#[test]
fn test_exchange_authorization_code() {
    let client = Client::with_application("myclientid", "myclientsecret");
    let resp = client.exchange_authorization_code("mycode", "http://example.com/cb");
    assert_eq!(resp.get("access_token").unwrap(), "myaccesstoken");
    assert_eq!(resp.get("refresh_token").unwrap(), "myrefreshtoken");
    assert_eq!(resp.get("scope").unwrap(), &serde_json::json!(["basicProfile"]));
}

#[test]
fn test_exchange_refresh_token() {
    let client = Client::with_application("myclientid", "myclientsecret");
    let resp = client.exchange_refresh_token("myrefreshtoken");
    assert_eq!(resp.get("access_token").unwrap(), "myaccesstoken2");
    assert_eq!(resp.get("refresh_token").unwrap(), "myrefreshtoken2");
    assert_eq!(resp.get("scope").unwrap(), &serde_json::json!(["basicProfile"]));
}

#[test]
fn test_get_current_user() {
    let client = Client::new("myaccesstoken");
    let resp = client.get_current_user();
    let expected = serde_json::json!({
        "username": "nicki",
        "url": "https://medium.com/@nicki",
        "imageUrl": "https://images.medium.com/0*fkfQiTzT7TlUGGyI.png",
        "id": "5303d74c64f66366f00cb9b2a94f3251bf5",
        "name": "Nicki Minaj",
    });
    for (k, v) in expected.as_object().unwrap() {
        assert_eq!(resp.get(k).unwrap(), v);
    }
}

#[test]
fn test_create_post() {
    let client = Client::new("myaccesstoken");
    let resp = client.create_post(
        "5303d74c64f66366f00cb9b2a94f3251bf5",
        "Starships",
        "<p>Are meant to flyyyy</p>",
        "html",
        &["stars", "ships", "pop"],
        "draft"
    );
    let expected = serde_json::json!({
        "license": "all-rights-reserved",
        "title": "Starships",
        "url": "https://medium.com/@nicki/55050649c95",
        "tags": ["stars", "ships", "pop"],
        "authorId": "5303d74c64f66366f00cb9b2a94f3251bf5",
        "publishStatus": "draft",
        "id": "55050649c95",
    });
    for (k, v) in expected.as_object().unwrap() {
        assert_eq!(resp.get(k).unwrap(), v);
    }
}

#[test]
fn test_upload_image() {
    let client = Client::new("myaccesstoken");
    let resp = client.upload_image("./tests/test.png", "image/png");
    let expected = serde_json::json!({
        "url": "https://cdn-images-1.medium.com/0*dlkfjalksdjfl.jpg",
        "md5": "d87e1628ca597d386e8b3e25de3a18bc",
    });
    for (k, v) in expected.as_object().unwrap() {
        assert_eq!(resp.get(k).unwrap(), v);
    }
}