use ai_models::checkpoint::*;
use std::collections::HashMap;
use tempfile::tempdir;
use std::fs::File;
use std::io::Write;

fn save_checkpoint(obj: &AnyValue, path: &std::path::Path) {
    let mut f = File::create(path).unwrap();
    let buf = serde_pickle::to_vec(obj, true).unwrap();
    f.write_all(&buf).unwrap();
}

fn load_checkpoint(path: &std::path::Path) -> AnyValue {
    let buf = std::fs::read(path).unwrap();
    serde_pickle::from_slice(&buf).unwrap()
}

#[test]
fn test_public_checkpoint_create_and_load() {
    let data = AnyValue::Map({
        let mut m = HashMap::new();
        m.insert("epoch".to_string(), AnyValue::Int(7));
        m.insert("val_loss".to_string(), AnyValue::Float(0.024));
        m
    });
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("cpoint_pub.pt");
    save_checkpoint(&data, &file_path);
    let loaded = load_checkpoint(&file_path);
    if let AnyValue::Map(ref m) = loaded {
        assert_eq!(m.get("epoch"), Some(&AnyValue::Int(7)));
        assert_eq!(m.get("val_loss"), Some(&AnyValue::Float(0.024)));
        assert_ne!(m, &{
            let mut m = HashMap::new();
            m.insert("epoch".to_string(), AnyValue::Int(10));
            m.insert("val_loss".to_string(), AnyValue::Float(0.01));
            m
        });
    } else {
        panic!("Loaded checkpoint not a map");
    }
}