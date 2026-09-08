use std::fs;
use std::path::Path;

use gvanim::render;

#[test]
fn test_render_tmp() {
    let tmp_dir = tempfile::tempdir().unwrap();
    let out_prefix = tmp_dir.path().join("myanim").to_str().unwrap().to_string();

    // Prepare dummy graphs
    let files = render::render(&["digraph{}", "digraph{}"], &out_prefix, "dot", 10);
    assert_eq!(files.len(), 2);

    for file in &files {
        assert!(Path::new(&file).exists());
    }
}

#[test]
fn test_gif() {
    let tmp_dir = tempfile::tempdir().unwrap();
    let mut files = vec![];
    for i in 0..2 {
        let f = tmp_dir.path().join(format!("f{}.png", i));
        fs::write(&f, b"test").unwrap();
        files.push(f.to_str().unwrap().to_string());
    }

    // Just test that gif() does not error if files exist
    assert!(render::gif(&files, &(tmp_dir.path().join("anim").to_str().unwrap()), 123, 11).is_ok());
}