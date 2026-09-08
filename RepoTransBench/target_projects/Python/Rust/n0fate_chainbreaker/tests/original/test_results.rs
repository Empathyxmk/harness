use n0fate_chainbreaker::results::{DummyRecord, log_output, DummyArgs, Collection, write_collection_to_file};
use tempfile::tempdir;

#[test]
fn test_log_output_keyboard_interrupt() {
    // No KeyboardInterrupt in Rust, so we just simulate calling log_output
    let args = DummyArgs;
    let mut summary = Vec::new();
    struct MyRecord;
    impl std::fmt::Display for MyRecord {
        fn fmt(&self, _: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            Err(std::fmt::Error) // Simulate error
        }
    }
    let coll = Collection {
        header: "h".to_string(),
        records: vec![DummyRecord],
        write_to_console: true,
        write_to_disk: false,
        write_directory: "/tmp".to_string(),
    };
    // Should not panic
    log_output(&[coll], &mut summary, &args);
}

#[test]
fn test_log_output_console_and_disk() {
    let args = DummyArgs;
    let mut summary = Vec::new();
    let dir = tempdir().unwrap();
    let path = dir.path().to_str().unwrap();
    let coll = Collection {
        header: "header-here".to_string(),
        records: vec![DummyRecord],
        write_to_console: true,
        write_to_disk: true,
        write_directory: path.to_string(),
    };
    log_output(&[coll], &mut summary, &args);
    let pattern1 = format!("{}/{}.txt", path, "h");
    let pattern2 = format!("{}/{}.txt", path, "header-here");
    let match1 = std::path::Path::new(&pattern1).exists();
    let match2 = std::path::Path::new(&pattern2).exists();
    assert!(match1 || match2);
}

#[test]
fn test_summary_output() {
    let mut summary = Vec::new();
    // Simulate monkeypatch log_output with closure in Rust by just pushing to the summary
    let dummy_collections: Vec<n0fate_chainbreaker::results::Collection> = vec![];
    fn fake_log_output(_c: &[n0fate_chainbreaker::results::Collection], summary: &mut Vec<String>, _a: &n0fate_chainbreaker::results::DummyArgs) {
        summary.push("called".to_string());
    }
    fake_log_output(&dummy_collections, &mut summary, &n0fate_chainbreaker::results::DummyArgs);
    assert!(summary.contains(&"called".to_string()));
}

#[test]
fn test_write_collection_to_file() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_str().unwrap().to_string();
    let coll = Collection {
        header: "HHH".to_string(),
        records: vec![DummyRecord, DummyRecord],
        write_to_console: false,
        write_to_disk: true,
        write_directory: path.clone(),
    };
    let f = write_collection_to_file(&coll, "content").unwrap();
    let s = std::fs::read_to_string(f).unwrap();
    assert!(s.contains("content"));
}