use chrono::{TimeZone, Utc};
use std::collections::HashMap;
use owncloud_pyocclient::owncloud::*;
use std::any::Any;

#[test]
fn test_init_with_int() {
    let err = ResponseError::new_raw(404, "MyErr");
    assert_eq!(err.status_code, Some(404));
    assert_eq!(format!("{}", err), "MyErr error: 404");
}

#[test]
fn test_init_with_response() {
    #[derive(Debug, Clone)]
    struct FakeRes {
        status_code: u16,
        content: Vec<u8>,
    }
    let res = FakeRes { status_code: 400, content: b"resbody".to_vec() };
    let err = ResponseError {
        status_code: Some(res.status_code),
        message: Some("OCS".to_string()),
        resource_body: Some(ResourceBody::Bytes(res.content.clone()))
    };
    assert_eq!(err.status_code, Some(400));
    assert_eq!(err.get_resource_body().unwrap(), b"resbody".as_ref());
    assert!(format!("{}", err).starts_with("OCS error: 400") || format!("{}", err).starts_with("HTTP error: 400 (OCS)"));
}

#[test]
fn test_init_with_response_strcontent() {
    #[derive(Debug, Clone)]
    struct FakeRes {
        status_code: u16,
        content: String,
    }
    let res = FakeRes { status_code: 501, content: "Some string".to_string() };
    let err = ResponseError {
        status_code: Some(res.status_code),
        message: Some("Txt".to_string()),
        resource_body: Some(ResourceBody::String(res.content.clone())),
    };
    assert_eq!(err.status_code, Some(501));
    assert_eq!(err.get_resource_body().unwrap(), "Some string");
    assert!(format!("{:?}", err).contains("Some string") || format!("{}", err).contains("Some string"));
}

#[test]
fn test_repr_and_branching() {
    let rr = ResponseError::new_raw(401, "");
    assert!(format!("{}", rr) == " error: 401" || format!("{}", rr) == "HTTP error: 401");

    // test with no content property in response
    #[derive(Debug, Clone)]
    struct FakeRes {
        status_code: u16,
    }
    let err2 = ResponseError {
        status_code: Some(500),
        message: None,
        resource_body: None
    };
    assert!(err2.get_resource_body().is_none());
    assert!(format!("{}", err2).contains("HTTP error: 500"));
}

#[test]
fn test_ocs_xml_msg() {
    #[derive(Debug, Clone)]
    struct FakeRes {
        status_code: u16,
        content: Vec<u8>,
    }
    let res = FakeRes {
        status_code: 500,
        content: b"<root><message>failmsg</message></root>".to_vec(),
    };
    let err = OCSResponseError::new(Some(res.status_code), Some(ResourceBody::Bytes(res.content.clone())));
    assert!(format!("{}", err).contains("failmsg"));
    assert_eq!(err.get_resource_body().unwrap(), b"<root><message>failmsg</message></root>".as_ref());
}

#[test]
fn test_ocs_xml_invalid() {
    #[derive(Debug, Clone)]
    struct FakeRes {
        status_code: u16,
        content: Vec<u8>,
    }
    let res = FakeRes {
        status_code: 400,
        content: b"not<xml".to_vec(),
    };
    let err = OCSResponseError::new(Some(res.status_code), Some(ResourceBody::Bytes(res.content.clone())));
    assert!(format!("{}", err).contains("OCS response error"));
    assert_eq!(err.get_resource_body().unwrap(), b"not<xml".as_ref());
}

#[test]
fn test_ocs_none() {
    let err = OCSResponseError::new(None, None);
    assert!(err.get_resource_body().is_none());
}

fn make_shareinfo(info: &[(&str, &str)]) -> ShareInfo {
    let map = info.iter().map(|(k, v)| (k.to_string(), v.to_string())).collect();
    ShareInfo::new(map)
}

#[test]
fn test_getters() {
    let mut info = HashMap::new();
    info.insert("id".to_string(), "123".to_string());
    info.insert("share_type".to_string(), "1".to_string());
    info.insert("permissions".to_string(), "3".to_string());
    info.insert("share_with".to_string(), "user1".to_string());
    info.insert("share_with_displayname".to_string(), "User One".to_string());
    info.insert("stime".to_string(), "1777777700".to_string());
    info.insert("expiration".to_string(), "2024-12-31".to_string());
    info.insert("path".to_string(), "/some.txt".to_string());
    let share = ShareInfo::new(info);

    assert_eq!(share.get_id(), Some(123));
    assert_eq!(share.get_share_type(), Some(1));
    assert_eq!(share.get_share_with().unwrap(), "user1");
    assert_eq!(share.get_share_with_displayname().unwrap(), "User One");
    assert_eq!(share.get_path().unwrap(), "/some.txt");
    assert_eq!(share.get_expiration().unwrap(), "2024-12-31");
    assert!(share.get_share_time().is_some());
}

#[test]
fn test_int_conversion() {
    let mut info = HashMap::new();
    info.insert("id".to_string(), "123".to_string());
    info.insert("permissions".to_string(), "".to_string());
    info.insert("stime".to_string(), "1777777700".to_string());
    // share_type purposely omitted or set None
    let share = ShareInfo::new(info);

    assert_eq!(share._get_int("id"), Some(123));
    assert_eq!(share._get_int("permissions"), None);
    assert_eq!(share._get_int("share_type"), None);
    let dt = share.get_share_time();
    assert!(dt.is_some());
}

#[test]
fn test_missing_attrs() {
    let share = ShareInfo::new(HashMap::new());
    assert!(share.get_share_with().is_none());
    assert!(share.get_share_with_displayname().is_none());
    assert!(share.get_path().is_none());
}

#[test]
fn test_del_attrs_removed() {
    let mut input_info = HashMap::new();
    input_info.insert("id".to_string(), "1".to_string());
    input_info.insert("storage".to_string(), "xxx".to_string());
    input_info.insert("mail_send".to_string(), "1".to_string());
    input_info.insert("item_type".to_string(), "foo".to_string());
    input_info.insert("item_source".to_string(), "42".to_string());
    input_info.insert("file_source".to_string(), "15".to_string());
    input_info.insert("parent".to_string(), "".to_string());
    input_info.insert("other".to_string(), "ok".to_string());
    input_info.insert("stime".to_string(), "1000".to_string());
    let mut share = ShareInfo::new(input_info);

    share.del_attrs();
    assert!(!share.share_info.contains_key("item_type"));
    assert!(!share.share_info.contains_key("parent"));
    assert!(share.share_info.contains_key("id"));
}

#[test]
fn test_contains_and_getitem() {
    let mut map = HashMap::new();
    map.insert("id".to_string(), "99".to_string());
    map.insert("foo".to_string(), "bar".to_string());
    let share = ShareInfo::new(map);
    assert!(share.share_info.contains_key("id"));
    assert_eq!(share["foo"], "bar");
}

#[test]
fn test_escape_unescape() {
    let p = "/a b/abc.txt";
    let out = escape_path(p);
    assert!(out.contains("%20"));
    assert_eq!(unescape_path(&out), p);
}

#[test]
fn test_to_unicode_bytes() {
    assert_eq!(to_unicode(b"abc".as_ref()), "abc");
    assert_eq!(to_unicode("xyz"), "xyz");
}

#[test]
fn test_to_bytes() {
    assert_eq!(to_bytes("xyz"), b"xyz".to_vec());
    assert_eq!(to_bytes(b"xyz".as_ref()), b"xyz".to_vec());
}

#[test]
fn test_strip_trailing_slash() {
    assert_eq!(strip_trailing_slash(Some("foo/")).unwrap(), "foo");
    assert_eq!(strip_trailing_slash(Some("/bar/")).unwrap(), "/bar");
    assert_eq!(strip_trailing_slash(Some("/")).unwrap(), "/");
    assert_eq!(strip_trailing_slash(None), None);
}