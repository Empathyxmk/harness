use crate::extract::*;
use std::collections::HashMap;

#[test]
fn test_pad_and_concat_basic() {
    let arr1 = vec![vec![0.0,0.0],vec![0.0,0.0]];
    let arr2 = vec![vec![1.0,1.0],vec![1.0,1.0]];
    let arrs = vec![arr1.clone(), arr2.clone()];
    let result = pad_and_concat(&arrs, 0);
    assert_eq!(result.len(), 4);
    assert_eq!(result[0], vec![0.0,0.0]);
    assert_eq!(result[2], vec![1.0,1.0]);
}

#[test]
fn test_pad_and_concat_different_shapes() {
    let arr1 = vec![vec![0.0,0.0],vec![0.0,0.0]];
    let arr2 = vec![vec![1.0,1.0],vec![1.0,1.0],vec![1.0,1.0]];
    let arrs = vec![arr1, arr2];
    let result = pad_and_concat(&arrs, 0);
    assert_eq!(result.len(), 5);
}

#[test]
fn test_flatten_dict() {
    let mut d = HashMap::new();
    d.insert("a".to_string(), 1);
    d.insert("b".to_string(), 2);
    let (keys, vals) = flatten_dict(&d);
    assert!(keys.contains(&"a".to_string()));
    assert!(vals.contains(&1));
}

#[test]
fn test_shape_returns_correct() {
    let arr = vec![vec![vec![0.0; 4]; 3]; 2];
    let shape = shape(&arr);
    assert_eq!(shape, (2,3,4));
    let arr2 = vec![vec![0.0; 3]; 2];
    assert_eq!((2,3), (arr2.len(), arr2[0].len()));
}

#[test]
fn test_shape_empty() {
    let arr: Vec<Vec<Vec<f64>>> = Vec::new();
    let sh = shape(&arr);
    assert_eq!(sh, (0,0,0));
}

#[test]
fn test_parse_bvh_hierarchy_and_motion() {
    let text = 
r#"HIERARCHY
ROOT Hips
{
    OFFSET 0.00 0.00 0.00
    CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
    JOINT Knee
    {
        OFFSET 0.00 1.00 0.00
        CHANNELS 3 Zrotation Xrotation Yrotation
    }
}
MOTION
Frames: 2
Frame Time: 0.0333333
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
1.0 1.0 1.0 0.5 0.5 0.5 0.1 0.2 0.3
"#;
    let lines: Vec<_> = text.lines().map(str::to_string).collect();
    let parsed = parse_bvh(&lines).unwrap();
    assert!(parsed.contains_key("hierarchy"));
    assert!(parsed.contains_key("motion"));
    assert!(parsed.get("motion").unwrap().len() == 2);
    assert!(parsed.contains_key("channels"));
}

#[test]
#[should_panic]
fn test_parse_bvh_malformed() {
    let lines = vec!["nonsense".to_string(), "not bvh".to_string()];
    let _ = parse_bvh(&lines).unwrap();
}