use serde_json::json;

fn make_literal(val: serde_json::Value) -> serde_json::Value {
    json!({"type": "literal", "value": val, "children": []})
}

#[test]
fn test_comparator() {
    let left = make_literal(json!(1));
    let right = make_literal(json!(2));
    let c = json!({"type": "comparator", "children": [left.clone(), right.clone()], "value": "eq"});
    assert_eq!(c["type"], "comparator");
    assert_eq!(c["children"][0]["value"], 1);
    assert_eq!(c["value"], "eq");
}

#[test]
fn test_current_node() {
    let c = json!({"type": "current", "children": []});
    assert_eq!(c["type"], "current");
    assert_eq!(c["children"], json!([]));
}

#[test]
fn test_expref() {
    let inner = json!({"type": "identity", "children": []});
    let e = json!({"type": "expref", "children": [inner.clone()]});
    assert_eq!(e["type"], "expref");
    assert_eq!(e["children"][0]["type"], "identity");
}

#[test]
fn test_function_expression() {
    let fe = json!({"type": "function_expression", "value": "foo", "children": [make_literal(json!(1))]});
    assert_eq!(fe["type"], "function_expression");
    assert_eq!(fe["value"], "foo");
    assert_eq!(fe["children"][0]["value"], 1);
}

#[test]
fn test_field() {
    let f = json!({"type": "field", "value": "foo"});
    assert_eq!(f["type"], "field");
    assert_eq!(f["value"], "foo");
}

#[test]
fn test_filter_projection() {
    let ident = json!({"type": "identity", "children": []});
    let foo = json!({"type": "foo", "children": []});
    let bar = json!({"type": "bar", "children": []});
    let fp = json!({"type": "filter_projection", "children": [ident.clone(), foo.clone(), bar.clone()]});
    assert_eq!(fp["type"], "filter_projection");
    assert_eq!(fp["children"].as_array().unwrap().len(), 3);
}

#[test]
fn test_flatten() {
    let node = json!({"type": "identity", "children": []});
    let flat = json!({"type": "flatten", "children": [node.clone()]});
    assert_eq!(flat["type"], "flatten");
    assert_eq!(flat["children"][0], node);
}

#[test]
fn test_identity() {
    let node = json!({"type": "identity", "children": []});
    assert_eq!(node["type"], "identity");
    assert_eq!(node["children"], json!([]));
}

#[test]
fn test_index() {
    let node = json!({"type": "index", "value": 3});
    assert_eq!(node["type"], "index");
    assert_eq!(node["value"], 3);
}

#[test]
fn test_index_expression() {
    let a_literal = make_literal(json!("a"));
    let node = json!({"type": "index_expression", "children": [a_literal.clone()]});
    assert_eq!(node["type"], "index_expression");
    assert_eq!(node["children"][0]["value"], "a");
}

#[test]
fn test_key_val_pair() {
    let child = make_literal(json!(42));
    let node = json!({"type": "key_val_pair", "value": "k", "children": [child.clone()]});
    assert_eq!(node["type"], "key_val_pair");
    assert_eq!(node["value"], "k");
    assert_eq!(node["children"][0]["value"], 42);
}

#[test]
fn test_literal() {
    let l = make_literal(json!({"foo": "bar"}));
    assert_eq!(l["type"], "literal");
    assert_eq!(l["value"], json!({"foo": "bar"}));
}

#[test]
fn test_multi_select_dict() {
    let nodes = vec![make_literal(json!(3))];
    let m = json!({"type": "multi_select_dict", "children": nodes.clone()});
    assert_eq!(m["type"], "multi_select_dict");
    assert_eq!(m["children"], json!(nodes));
}

#[test]
fn test_multi_select_list() {
    let nodes = vec![make_literal(json!(5))];
    let m = json!({"type": "multi_select_list", "children": nodes.clone()});
    assert_eq!(m["type"], "multi_select_list");
    assert_eq!(m["children"], json!(nodes));
}

#[test]
fn test_or_expression() {
    let a = make_literal(json!(1));
    let b = make_literal(json!(2));
    let node = json!({"type": "or_expression", "children": [a.clone(), b.clone()]});
    assert_eq!(node["type"], "or_expression");
    assert_eq!(node["children"][0]["value"], 1);
}

#[test]
fn test_and_expression() {
    let a = make_literal(json!(1));
    let b = make_literal(json!(2));
    let node = json!({"type": "and_expression", "children": [a.clone(), b.clone()]});
    assert_eq!(node["type"], "and_expression");
    assert_eq!(node["children"][1]["value"], 2);
}

#[test]
fn test_not_expression() {
    let a = make_literal(json!(false));
    let node = json!({"type": "not_expression", "children": [a.clone()]});
    assert_eq!(node["type"], "not_expression");
    assert_eq!(node["children"][0]["value"], false);
}

#[test]
fn test_pipe() {
    let l = make_literal(json!(1));
    let r = make_literal(json!(2));
    let p = json!({"type": "pipe", "children": [l.clone(), r.clone()]});
    assert_eq!(p["type"], "pipe");
    assert_eq!(p["children"][1]["value"], 2);
}

#[test]
fn test_projection() {
    let l = make_literal(json!(1));
    let r = make_literal(json!(2));
    let p = json!({"type": "projection", "children": [l.clone(), r.clone()]});
    assert_eq!(p["type"], "projection");
    assert_eq!(p["children"][0]["value"], 1);
    assert_eq!(p["children"][1]["value"], 2);
}

#[test]
fn test_subexpression() {
    let c1 = make_literal(json!(1));
    let c2 = make_literal(json!(2));
    let children = vec![c1.clone(), c2.clone()];
    let s = json!({"type": "subexpression", "children": children.clone()});
    assert_eq!(s["type"], "subexpression");
    assert_eq!(s["children"][1]["value"], 2);
}

#[test]
fn test_slice() {
    let node = json!({"type": "slice", "children": [json!(0), json!(10), json!(2)]});
    assert_eq!(node["type"], "slice");
    assert_eq!(node["children"].as_array().unwrap().len(), 3);
}

#[test]
fn test_value_projection() {
    let l = make_literal(json!(3));
    let r = make_literal(json!(4));
    let node = json!({"type": "value_projection", "children": [l.clone(), r.clone()]});
    assert_eq!(node["type"], "value_projection");
    assert_eq!(node["children"][1]["value"], 4);
}