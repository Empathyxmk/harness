use bdarnell_plop::callgraph::{CallGraph, Node};
use std::collections::HashMap;

#[test]
fn test_basic_attrs() {
    let mut graph = CallGraph::new();
    graph.add_stack(
        vec![Node::new(1), Node::new(2)],
        [("time", 1)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(1), Node::new(3)],
        [("time", 3)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(1), Node::new(2), Node::new(3)],
        [("time", 7)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(1), Node::new(4), Node::new(2), Node::new(3)],
        [("time", 2)].iter().cloned().collect(),
    );
    assert_eq!(graph.nodes.len(), 4);
    assert_eq!(graph.edges.len(), 5);
}

#[test]
fn test_top_edges() {
    let mut graph = CallGraph::new();
    graph.add_stack(
        vec![Node::new(1), Node::new(2)],
        [("time", 1)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(1), Node::new(3)],
        [("time", 3)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(1), Node::new(2), Node::new(3)],
        [("time", 7)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(1), Node::new(4), Node::new(2), Node::new(3)],
        [("time", 2)].iter().cloned().collect(),
    );
    let top_edges = graph.get_top_edges("time", 3);
    let summary: Vec<(i32, i32, i32)> = top_edges
        .iter()
        .map(|e| (e.parent.id, e.child.id, *e.weights.get("time").unwrap_or(&0)))
        .collect();
    assert_eq!(
        summary,
        vec![(2, 3, 9), (1, 2, 8), (1, 3, 3)]
    );
}

#[test]
fn test_top_nodes() {
    let mut graph = CallGraph::new();
    graph.add_stack(
        vec![Node::new(1), Node::new(2)],
        [("time", 1)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(1), Node::new(3)],
        [("time", 3)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(1), Node::new(2), Node::new(3)],
        [("time", 7)].iter().cloned().collect(),
    );
    graph.add_stack(
        vec![Node::new(1), Node::new(4), Node::new(2), Node::new(3)],
        [("time", 2)].iter().cloned().collect(),
    );
    let top_nodes = graph.get_top_nodes("time", 2);
    let summary: Vec<(i32, i32)> = top_nodes
        .iter()
        .map(|n| (n.id, *n.weights.get("time").unwrap_or(&0)))
        .collect();
    assert_eq!(summary, vec![(3, 12), (2, 1)]);
}