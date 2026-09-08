use bdarnell_plop::callgraph::{CallGraph, Node};
use std::collections::HashMap;

#[test]
fn test_public_basic_attrs() {
    let mut graph = CallGraph::new();
    graph.add_stack(
        vec![Node::new(10), Node::new(20)],
        [("weight", 2)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(10), Node::new(30)],
        [("weight", 8)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(10), Node::new(20), Node::new(30)],
        [("weight", 4)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(18), Node::new(10), Node::new(40)],
        [("weight", 6)].iter().cloned().collect(),
    );
    assert_eq!(graph.nodes.len(), 4);
    assert_eq!(graph.edges.len(), 5);
}

#[test]
fn test_public_top_edges() {
    let mut graph = CallGraph::new();
    graph.add_stack(
        vec![Node::new(10), Node::new(20)],
        [("weight", 2)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(10), Node::new(30)],
        [("weight", 8)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(10), Node::new(20), Node::new(30)],
        [("weight", 4)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(18), Node::new(10), Node::new(40)],
        [("weight", 6)].iter().cloned().collect(),
    );
    let top_edges = graph.get_top_edges("weight", 2);
    let summary: Vec<(i32, i32, i32)> = top_edges
        .iter()
        .map(|e| (e.parent.id, e.child.id, *e.weights.get("weight").unwrap_or(&0)))
        .collect();
    assert_eq!(
        summary,
        vec![(10, 30, 12), (10, 20, 6)]
    );
}

#[test]
fn test_public_top_nodes() {
    let mut graph = CallGraph::new();
    graph.add_stack(
        vec![Node::new(10), Node::new(20)],
        [("weight", 2)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(10), Node::new(30)],
        [("weight", 8)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(10), Node::new(20), Node::new(30)],
        [("weight", 4)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(18), Node::new(10), Node::new(40)],
        [("weight", 6)].iter().cloned().collect(),
    );
    let top_nodes = graph.get_top_nodes("weight", 3);
    let summary: Vec<(i32, i32)> = top_nodes
        .iter()
        .map(|n| (n.id, *n.weights.get("weight").unwrap_or(&0)))
        .collect();
    assert_eq!(summary, vec![(30, 12), (10, 0), (20, 2)]);
}