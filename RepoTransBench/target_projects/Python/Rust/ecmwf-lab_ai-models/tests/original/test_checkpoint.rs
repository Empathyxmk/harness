use ai_models::checkpoint::*;
use std::collections::HashMap;

#[test]
fn test_tidy_dict_and_list_tuple() {
    let mut m = HashMap::new();
    m.insert("a".to_string(), AnyValue::List(vec![
        AnyValue::Int(1),
        AnyValue::Int(2),
        AnyValue::Map({
            let mut b = HashMap::new();
            b.insert("b".to_string(), AnyValue::Tuple(vec![AnyValue::Int(3), AnyValue::Null]));
            b
        }),
    ]));
    m.insert("c".to_string(), AnyValue::Tuple(vec![AnyValue::Int(4), AnyValue::Int(5)]));
    let orig = AnyValue::Map(m.clone());
    let result = tidy(&orig);
    assert_eq!(result, AnyValue::Map(m));
}

#[test]
fn test_tidy_base_types() {
    let vals = vec![
        AnyValue::Null,
        AnyValue::Int(3),
        AnyValue::Float(0.1),
        AnyValue::String("foo".into()),
        AnyValue::Bool(true),
    ];
    for v in vals.iter() {
        assert_eq!(tidy(v), v.clone());
    }
}

#[test]
fn test_tidy_unknown_type() {
    let v = AnyValue::List(vec![]);
    assert_eq!(tidy(&v), v.clone());
}

#[test]
fn test_FakeStorage_construction() {
    let s = FakeStorage::new();
    assert_eq!(s.dtype, "float32");
}

#[test]
fn test_UnpicklerWrapper() {
    let uw = UnpicklerWrapper::new(vec![]);
    let res = uw.persistent_load("id");
    assert_eq!(res.dtype, "float32");
}

use std::fs::File;
use tempfile::tempdir;
use std::io::Write;

fn make_zip_with_data_pkl(obj: &AnyValue, filename: &str, extra: bool) -> String {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("data.zip");
    let f = File::create(&file_path).unwrap();
    let mut zip = zip::ZipWriter::new(f);
    let options = zip::write::FileOptions::default();
    zip.start_file(filename, options).unwrap();
    let buf = serde_pickle::to_vec(obj, true).unwrap();
    zip.write_all(&buf).unwrap();
    if extra {
        zip.start_file("data2.pkl", options).unwrap();
        zip.write_all(b"otherdata").unwrap();
    }
    zip.finish().unwrap();
    file_path.to_str().unwrap().to_owned()
}

#[test]
fn test_peek_single_data_pkl() {
    let obj = AnyValue::Map({
        let mut m = HashMap::new();
        m.insert("foo".to_string(), AnyValue::Int(1));
        m
    });
    let zfile = make_zip_with_data_pkl(&obj, "data.pkl", false);
    let result = peek(&zfile).expect("peek failed");
    if let AnyValue::Map(m) = result {
        assert!(m.get("foo") == Some(&AnyValue::Int(1)));
    } else {
        panic!("Result not a map");
    }
}

#[test]
fn test_peek_duplicate_data_pkl() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("dupdata.zip");
    let f = File::create(&file_path).unwrap();
    let mut zip = zip::ZipWriter::new(f);
    let options = zip::write::FileOptions::default();
    zip.start_file("first/data.pkl", options).unwrap();
    zip.write_all(&serde_pickle::to_vec(&AnyValue::Map(HashMap::new()), true).unwrap()).unwrap();
    zip.start_file("second/data.pkl", options).unwrap();
    zip.write_all(&serde_pickle::to_vec(&AnyValue::Map(HashMap::new()), true).unwrap()).unwrap();
    zip.finish().unwrap();

    let result = peek(&file_path);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Found two data.pkl"));
}