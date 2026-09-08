use pywizlight_rust::scenes::*;

#[tokio::test]
async fn test_get_id_from_scene_name_not_found() {
    let err = get_id_from_scene_name("non_exist");
    assert!(err.is_err());
}

#[tokio::test]
async fn test_get_id_from_scene_name_alarm() {
    let scene_id = get_id_from_scene_name("Alarm").unwrap();
    assert_eq!(scene_id, 35);
}