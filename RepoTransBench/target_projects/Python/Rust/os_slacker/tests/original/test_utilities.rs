use os_slacker::utilities::get_item_id_by_name;
use serde_json::json;

#[test]
fn test_get_item_id_by_name() {
    let list_dict = vec![
        serde_json::json!({"name": "channel_name", "id": "123"}).as_object().unwrap().clone(),
        serde_json::Map::new(),
    ];
    let result = get_item_id_by_name(&list_dict, "channel_name");
    assert_eq!(result.as_deref(), Some("123"));
}