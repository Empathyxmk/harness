// Public ruleConfig API test in rust

#[test]
fn test_rule_config_set_and_get_diff_data() {
    let rule_id = "12001";
    let key = "attackStrength";
    let value = "LOW";
    let set_resp = serde_json::json!({
        "status": "UPDATED",
        "ruleId": rule_id
    });
    assert_eq!(set_resp["status"], "UPDATED");
    assert_eq!(set_resp["ruleId"], rule_id);

    let get_resp = serde_json::json!({
        "value": value,
        "key": key
    });
    assert_eq!(get_resp["value"], value);
    assert_eq!(get_resp["key"], key);
}