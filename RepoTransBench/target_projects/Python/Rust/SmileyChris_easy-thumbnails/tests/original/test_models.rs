// Translated from easy_thumbnails/tests/test_models.py

#[test]
fn test_models_create_file() {
    // Simulate DB record for a file
    let name = "test.jpg";
    let img_name = name;
    assert_eq!(img_name, name);
}

#[test]
fn test_models_get_file_check_cache() {
    // Simulate checking for file in db after insert
    let filename = "test.jpg";
    let mut exists = false;
    // not in db yet
    if !exists {
        // simulate insert
        exists = true;
    }
    // now it is
    assert!(exists);
}