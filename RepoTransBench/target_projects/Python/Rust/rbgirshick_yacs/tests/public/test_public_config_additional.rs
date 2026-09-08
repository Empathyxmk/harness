use std::fs;
use std::io::Write;
use tempfile::tempdir;

use rbgirshick_yacs::config::*;

#[test]
fn test_load_cfg_yaml_and_py() {
    // YAML file test - different content
    let temp = tempdir().unwrap();
    let yaml_content = r#"
    K: 789
    L:
      M: false
    "#;
    let yaml_file = temp.path().join("test_diff.yaml");
    fs::write(&yaml_file, yaml_content).unwrap();
    let mut cfg = CfgNode::new(true);
    cfg.merge_from_file(&yaml_file).unwrap();
    assert_eq!(cfg.get_attr("K").unwrap().as_i64().unwrap(), 789);

    let l = match cfg.get_attr("L").unwrap() {
        ConfigValue::Map(map) => map,
        _ => panic!("L must be a map"),
    };
    assert_eq!(
        l.get("M").unwrap().as_bool().unwrap(),
        false
    );

    // Python file test (must define variable 'cfg' at top-level!)
    let py_content = r#"cfg = dict(Z=[7,8,9], Y=dict(X='baz'))"#;
    let py_file = temp.path().join("f2.py");
    fs::write(&py_file, py_content).unwrap();
    let mut cfg2 = CfgNode::new(true);
    cfg2.merge_from_file(&py_file).unwrap();
    // assert cfg2.Z == [7,8,9]
    let z = cfg2.get_attr("Z").unwrap();
    assert_eq!(
        z.as_vec().unwrap().iter().map(|v| v.as_i64().unwrap()).collect::<Vec<_>>(),
        vec![7,8,9]
    );
    // assert cfg2.Y.X == 'baz'
    let y = match cfg2.get_attr("Y").unwrap() {
        ConfigValue::Map(map) => map,
        _ => panic!("Y must be a map"),
    };
    assert_eq!(
        y.get("X").unwrap().as_str().unwrap(),
        "baz"
    );
}

#[test]
fn test_load_cfg_file_object_yaml() {
    let yaml_str = "A: 88\nB: [4, 5, 6]";
    let map: serde_yaml::Value = serde_yaml::from_str(yaml_str).unwrap();
    let dct = value_to_cfg(map);
    let mut cfg = CfgNode::new(true);
    cfg.merge_from_other_cfg(&dct);
    assert_eq!(cfg.get_attr("A").unwrap().as_i64().unwrap(), 88);
    let b = cfg.get_attr("B").unwrap();
    assert_eq!(b.as_vec().unwrap().iter().map(|v| v.as_i64().unwrap()).collect::<Vec<_>>(), vec![4,5,6]);
}

#[test]
fn test_load_cfg_file_object_py() {
    let temp = tempdir().unwrap();
    let py_content = r#"ALPHA = [100,200,300]"#;
    let py_file = temp.path().join("f_obj.py");
    fs::write(&py_file, py_content).unwrap();
    let mut cfg = CfgNode::new(true);
    cfg.merge_from_file(&py_file).unwrap();
    let a = cfg.get_attr("ALPHA").unwrap();
    assert_eq!(a.as_vec().unwrap().iter().map(|v| v.as_i64().unwrap()).collect::<Vec<_>>(), vec![100,200,300]);
}

#[test]
fn test_dump_and_load_roundtrip() {
    let mut cfg = CfgNode::new(true);
    cfg.data.insert("foo".to_string(), ConfigValue::Int(21));
    cfg.data.insert("bar".to_string(), ConfigValue::String("hello world".to_string()));
    let text = cfg.dump();
    let temp = tempdir().unwrap();
    let dumped_file = temp.path().join("public_dumped.yaml");
    fs::write(&dumped_file, text).unwrap();
    let mut new_cfg = CfgNode::new(true);
    new_cfg.merge_from_file(&dumped_file).unwrap();
    assert_eq!(new_cfg.get_attr("foo").unwrap().as_i64().unwrap(), 21);
    assert_eq!(new_cfg.get_attr("bar").unwrap().as_str().unwrap(), "hello world");
}

#[test]
fn test_wrong_extension() {
    let temp = tempdir().unwrap();
    let file_path = temp.path().join("bad2.txt");
    fs::write(&file_path, "BAR=3").unwrap();
    let r = CfgNode::load_cfg(&file_path);
    assert!(r.is_err());
}