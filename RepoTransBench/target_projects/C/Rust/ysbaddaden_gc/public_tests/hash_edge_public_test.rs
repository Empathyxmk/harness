#[test]
fn test_hash_edge_cases_public() {
    use std::collections::HashMap;
    let mut h = HashMap::new();
    let k1 = 1337;
    let v1 = 1;
    let k2 = 7331;
    let v2 = 2;
    let k3 = 8888;
    let v3 = 3;
    h.insert(k1, v1);
    h.insert(k2, v2);
    h.insert(k3, v3);
    assert_eq!(h.get(&k1), Some(&v1));
    assert_eq!(h.get(&k2), Some(&v2));
    assert_eq!(h.get(&k3), Some(&v3));
    h.remove(&k2);
    assert_eq!(h.get(&k2), None);
}