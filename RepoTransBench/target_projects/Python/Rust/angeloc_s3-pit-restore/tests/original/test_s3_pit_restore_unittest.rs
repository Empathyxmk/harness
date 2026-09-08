// Rust translation of Python: tests/test_s3_pit_restore_unittest.py

use std::fs;
use std::path::Path;
use std::collections::HashSet;

use s3_pit_restore::TestS3PitRestore;

#[test]
fn test_TestS3PitRestore_generate_tree() {
    // Use tempdir for isolation.
    let tmp_dir = tempfile::tempdir().expect("Could not create temp dir");
    let tree_dir = tmp_dir.path().join("gen");
    fs::create_dir_all(&tree_dir).expect("failed to create tree dir");

    // Simulate Python ["hello", "world"]
    let folder_names = vec!["hello", "world"];

    // Use our fake module/stub implementation.
    let test_obj = TestS3PitRestore {};

    // Call function.
    test_obj
        .generate_tree(&tree_dir, &["hello", "world"])
        .expect("generate_tree failed");

    // Check we have 2 directories, each with file.
    let entries: Vec<_> = fs::read_dir(&tree_dir)
        .expect("could not read tree dir")
        .filter_map(|e| e.ok())
        .collect();

    assert_eq!(entries.len(), 2);

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