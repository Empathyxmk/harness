// Translated from public_tests/test_thumbnail_cleanup_public.py

#[test]
fn test_thumbnail_cleanup_files_to_remove_public() {
    let thumbnails = vec!["public_thumbnails/thumb1.jpg", "public_thumbnails/thumb2.png"];
    assert_eq!(thumbnails.len(), 2);
    assert!(thumbnails[0].ends_with(".jpg"));
    assert!(thumbnails[1].ends_with(".png"));
}