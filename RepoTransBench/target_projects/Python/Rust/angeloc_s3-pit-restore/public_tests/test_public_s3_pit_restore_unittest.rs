// Rust translation of Python: public_tests/test_public_s3_pit_restore_unittest.py

use std::fs;
use s3_pit_restore::TestS3PitRestore;

#[test]
fn test_TestS3PitRestore_generate_tree_public() {
    let tmp_dir = tempfile::tempdir().expect("Could not create temp dir");
    let tree_dir = tmp_dir.path().join("treepub");
    fs::create_dir_all(&tree_dir).expect("failed to create tree dir");

    // Use ["foo", "bar", "baz"] for this public test.
    let folder_names = vec!["foo", "bar", "baz"];
    let test_obj = TestS3PitRestore {};

    test_obj
        .generate_tree(&tree_dir, &["foo", "bar", "baz"])
        .expect("generate_tree failed");

    let entries: Vec<_> = fs::read_dir(&tree_dir)
        .expect("could not read tree dir")
        .filter_map(|e| e.ok())
        .collect();
    assert_eq!(entries.len(), 3);

    for ent in entries {
        let path = ent.path();
        assert!(path.is_dir());
        let files: Vec<_> = fs::read_dir(&path)
            .expect("inner read failed")
            .filter_map(|e| e.ok())
            .collect();
        assert_eq!(files.len(), 1);
    }
}