// Public automation API new data test in rust

#[test]
fn test_get_progress_different_data() {
    // Simulate a call that would return a progress
    let progress_id = 7;
    let response = serde_json::json!({"progress": 42, "id": progress_id});
    assert!(response.get("progress").is_some());
    assert_ne!(response["progress"], 0);
}