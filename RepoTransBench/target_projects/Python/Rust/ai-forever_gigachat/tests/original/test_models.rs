use ai_forever_gigachat::model::Model;

#[test]
fn test_model_init_and_fields() {
    let model = Model::new(
        "special_object",
        "test_id_2",
        1234567,
        "SuperGigaModel",
        "public_giga_owner"
    );
    assert_eq!(model.id, "test_id_2");
    assert_eq!(model.object, "special_object");
    assert_eq!(model.name, "SuperGigaModel");
    assert_eq!(model.owned_by, "public_giga_owner");
    assert!(model.created > 0);
    assert!(model.x_headers.is_none());
}

#[test]
fn test_model_str_and_repr_public() {
    let model = Model::new(
        "public_object",
        "AAA_public",
        1010101,
        "PublicModel",
        "someone_else"
    );
    let text = format!("{}", model);
    let rep = format!("{:?}", model);
    assert!(text.contains("AAA_public") || text.contains("PublicModel"));
    assert!(rep.contains("AAA_public") || rep.contains("PublicModel"));
}