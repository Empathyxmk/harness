use pywizlight_rust::scenes::get_scene_name_from_id;

#[test]
fn test_scene_ids_public() {
    // Uncommon/edge id
    assert!(get_scene_name_from_id(256).is_none());
    // known
    assert_eq!(get_scene_name_from_id(18), Some("Candlelight"));
}