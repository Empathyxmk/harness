#[cfg(test)]
mod tests {
    use super::super::super::src::graph::{Graph, DummyConnection};
    use super::super::super::src::node::Node;
    use super::super::super::src::edge::Edge;

    fn setup_graph() -> Graph {
        Graph::new("G", DummyConnection)
    }

    #[test]
    fn test_graph_add_node() {
        let g = setup_graph();
        let n = Node::new();
        g.add_node(n.clone());
        assert!(g.nodes.borrow().contains(&n));
    }
    #[test]
    fn test_graph_add_edge() {
        let g = setup_graph();
        let n1 = Node::new();
        let n2 = Node::new();
        g.add_node(n1.clone());
        g.add_node(n2.clone());
        let e = Edge::new(n1.clone(), Some("knows".into()), n2.clone());
        g.add_edge(e.clone());
        assert!(g.edges.borrow().contains(&e));
    }
    #[test]
    fn test_graph_commit() {
        let g = setup_graph();
        let n1 = Node::new();
        let n2 = Node::new();
        g.add_node(n1.clone());
        g.add_node(n2.clone());
        let e = Edge::new(n1.clone(), Some("knows".into()), n2.clone());
        g.add_edge(e.clone());
        assert_eq!(g.commit(), "EXECUTED");
    }
    #[test]
    fn test_graph_delete() {
        let g = setup_graph();
        assert_eq!(g.delete(), "EXECUTED");
    }
    #[test]
    fn test_graph_query() {
        let g = setup_graph();
        assert_eq!(g.query("MATCH (n) RETURN n"), "EXECUTED");
    }
}