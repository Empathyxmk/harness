use claude_to_chatgpt::models;

#[test]
fn test_models_list_exists() {
    assert_eq!(models::models_list().is_empty(), false);
}

#[test]
fn test_model_map_exists() {
    let mm = models::model_map();
    assert_eq!(mm.is_empty(), false);
}