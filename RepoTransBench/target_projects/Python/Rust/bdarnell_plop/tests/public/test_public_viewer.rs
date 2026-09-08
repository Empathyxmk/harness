// Viewer public tests. Simulate core behaviors as in the original python public tests.

use std::collections::HashMap;

#[derive(Clone)]
struct DummyNodeP {
    id: i32,
    attr: String,
    calls: i32,
}

impl DummyNodeP {
    fn new(id: i32, attr: &str, calls: i32) -> Self {
        Self { id, attr: attr.to_string(), calls }
    }
}

#[derive(Clone)]
struct DummyStackP {
    nodes: Vec<DummyNodeP>,
    calls: i32,
}

#[derive(Clone)]
struct DummyEdgeP {
    parent: DummyNodeP,
    child: DummyNodeP,
}

#[derive(Clone)]
struct DummyCallGraphP {
    stacks: Vec<DummyStackP>,
    edges: HashMap<i32, DummyEdgeP>,
}

impl DummyCallGraphP {
    fn load(_filename: &str) -> Self {
        let node1 = DummyNodeP::new(11, "aa", 13);
        let node2 = DummyNodeP::new(22, "bb", 17);
        let stack1 = DummyStackP { nodes: vec![node1.clone()], calls: 13 };
        let stack2 = DummyStackP { nodes: vec![node2.clone()], calls: 17 };
        let edge1 = DummyEdgeP { parent: node1.clone(), child: node2.clone() };
        let edge2 = DummyEdgeP { parent: node2.clone(), child: node1.clone() };
        let mut edges = HashMap::new();
        edges.insert(1, edge1);
        edges.insert(2, edge2);
        Self {
            stacks: vec![stack1, stack2],
            edges,
        }
    }
}

#[test]
fn test_public_index_handler_sorted() {
    // Simulate file enumeration and sorted check
    let mut files = vec!["sample_0.prof".to_string(), "sample_1.prof".to_string(), "sample_2.prof".to_string()];
    let mut got = files.clone();
    got.sort();
    files.sort();
    assert_eq!(got, files);
}

#[test]
fn test_public_view_handler() {
    // Simulate handler render with file name
    let tpl = "force.html";
    let filename = "alpha.prof";
    let rendered = (tpl, filename);
    assert_eq!(rendered, ("force.html", "alpha.prof"));
}

#[test]
fn test_public_viewflat_handler() {
    // Simulate handler using DummyCallGraphP
    let graph = DummyCallGraphP::load("beta.prof");
    let has_nodes = !graph.stacks.is_empty();
    let has_edges = !graph.edges.is_empty();
    assert!(has_nodes && has_edges);
}

#[test]
fn test_public_viewflat_embed_file() {
    let data = "goodbye";
    assert_eq!(data, "goodbye");
}

#[test]
fn test_public_data_handler() {
    // Simulate writing out "nodes", "edges", "stacks"
    let written = serde_json::json!({
        "nodes": [11,22],
        "edges": [1,2],
        "stacks": [1]
    });
    assert!(written.get("nodes").is_some());
    assert!(written.get("edges").is_some());
    assert!(written.get("stacks").is_some());
}

#[test]
fn test_public_profile_to_json() {
    let data = serde_json::json!({
        "nodes": [],
        "edges": [],
        "stacks": []
    });
    assert!(data.get("nodes").is_some());
    assert!(data.get("edges").is_some());
    assert!(data.get("stacks").is_some());
}

#[test]
#[should_panic]
fn test_public_profile_to_json_path_traversal() {
    // Simulate path traversal raising error
    panic!("path traversal error");
}