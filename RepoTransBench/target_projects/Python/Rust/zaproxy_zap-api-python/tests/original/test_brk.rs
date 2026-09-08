use zaproxy_zap_api_rust::zapv2::brk::{DummyZap, Brk};

fn setup_brk<'a>() -> Brk<'a> {
    let mut zap = Box::new(DummyZap::new());
    Brk::new(Box::leak(zap))
}

#[test]
fn test_is_break_all() {
    let mut brk = setup_brk();
    assert_eq!(brk.is_break_all(), "dummy");
}

#[test]
fn test_is_break_request() {
    let mut brk = setup_brk();
    assert_eq!(brk.is_break_request(), "dummy");
}

#[test]
fn test_is_break_response() {
    let mut brk = setup_brk();
    assert_eq!(brk.is_break_response(), "dummy");
}

#[test]
fn test_http_message() {
    let mut brk = setup_brk();
    assert_eq!(brk.http_message(), "dummy");
}

#[test]
fn test_brk_type_state() {
    let mut brk = setup_brk();
    let res = brk.brk("http-all", "true", None);
    assert_eq!(res, "dummy");
}

#[test]
fn test_brk_with_scope() {
    let mut brk = setup_brk();
    let res = brk.brk("http-request", "false", Some("myscope"));
    assert_eq!(res, "dummy");
}

#[test]
fn test_set_http_message_header_only() {
    let mut brk = setup_brk();
    let res = brk.set_http_message("header", None);
    assert_eq!(res, "dummy");
}

#[test]
fn test_set_http_message_header_and_body() {
    let mut brk = setup_brk();
    let res = brk.set_http_message("header", Some("body"));
    assert_eq!(res, "dummy");
}

#[test]
fn test_cont() {
    let mut brk = setup_brk();
    assert_eq!(brk.cont(), "dummy");
}

#[test]
fn test_step() {
    let mut brk = setup_brk();
    assert_eq!(brk.step(), "dummy");
}

#[test]
fn test_drop() {
    let mut brk = setup_brk();
    assert_eq!(brk.drop(), "dummy");
}

#[test]
fn test_add_http_breakpoint() {
    let mut brk = setup_brk();
    let res = brk.add_http_breakpoint("string", "url", "contains", false, false);
    assert_eq!(res, "dummy");
}

#[test]
fn test_remove_http_breakpoint() {
    let mut brk = setup_brk();
    let res = brk.remove_http_breakpoint("string", "url", "contains", false, false);
    assert_eq!(res, "dummy");
}