use claude_to_chatgpt::models;

#[test]
fn test_public_models_list_exists() {
    let list = models::models_list();
    assert!(list.iter().all(|x| x.is_ascii()));
}

#[test]
fn test_public_model_map_exists() {
    let mm = models::model_map();
    assert!(mm.iter().all(|(k, v)| k.is_ascii() && v.is_ascii()));
}