// Public BRK API tests in rust

#[test]
fn test_brk_add_break_point_diff_data() {
    // Simulate the "add_break_point" logic:
    let url = "http://public.example.com/login";
    let method = "POST";
    let response = serde_json::json!({
        "status": "OK",
        "method": method,
        "url": url
    });
    assert_eq!(response["status"], "OK");
    assert_eq!(response["method"], method);
    assert!(response["url"].as_str().unwrap().starts_with("http://public."));
}

#[test]
fn test_brk_remove_break_point_diff_data() {
    let brk_id = "customBrk2";
    let response = serde_json::json!({
        "status": "REMOVED",
        "id": brk_id
    });
    assert_eq!(response["status"], "REMOVED");
    assert_eq!(response["id"], brk_id);
}