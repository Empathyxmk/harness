use os_slacker::utilities::get_item_id_by_name;

#[test]
fn test_get_item_id_by_name() {
    let list_dict = vec![
        serde_json::json!({"name": "public_channel", "id": "789"}).as_object().unwrap().clone(),
        serde_json::json!({"name": "other", "id": "456"}).as_object().unwrap().clone(),
    ];
    let result = get_item_id_by_name(&list_dict, "public_channel");
    assert_eq!(result.as_deref(), Some("789"));
}