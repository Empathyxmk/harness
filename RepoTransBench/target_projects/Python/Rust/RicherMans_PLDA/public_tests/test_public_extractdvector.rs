use richer_mans_plda::extractdvector;
use ndarray::array;
use tempfile::tempdir;
use std::fs::File;
use serde_pickle;

#[test]
fn test_dummy_extract_public() {
    let x = array![[5.0, 7.0], [9.0, 11.0]];
    let v = extractdvector::dummy_extract_dvector(&x);
    assert!((v[0] - 7.0).abs() < 1e-8 && (v[1] - 9.0).abs() < 1e-8);
}

#[test]
fn test_main_usage_public() {
    let ret = extractdvector::main(&["extractdvector.py"]);
    assert_eq!(ret, 1);
}

#[test]
fn test_main_ok_public() {
    let tmpdir = tempdir().unwrap();
    let out_path = tmpdir.path().join("public_out.pkl");

    let out_path_str = out_path.to_str().unwrap();
    let ret = extractdvector::main(&["extractdvector.py", "dummy_in", out_path_str]);
    assert_eq!(ret, 0);

    let file = File::open(&out_path).unwrap();
    let arr: Vec<f64> = serde_pickle::from_reader(file).unwrap();
    assert!((arr[0] - 2.0).abs() < 1e-8 && (arr[1] - 3.0).abs() < 1e-8);
}