#[cfg(test)]
mod tests {
    use super::super::super::src::node::Node;
    use super::super::super::src::edge::Edge;
    use super::super::super::src::path::Path;

    #[test]
    fn test_init() {
        let p = Path::new(vec![], vec![]);
        assert_eq!(p.nodes.len(), 0);
        assert_eq!(p.edges.len(), 0);
    }

    #[test]
    fn test_new_empty_path() {
        let p = Path::new_empty_path();
        assert_eq!(p.nodes.len(), 0);
        assert_eq!(p.edges.len(), 0);
    }

    #[test]
    fn test_nodes_and_edges() {
        let n1 = Node::id(1);
        let n2 = Node::id(2);
        let e1 = Edge::new(n1.clone(), None, n2.clone());
        let mut p = Path::new_empty_path();
        p = p.add_node(n1.clone());
        assert!(p.nodes.len() > 0);
        p = p.add_edge(e1.clone());
        assert!(p.edges.len() > 0);
        p = p.add_node(n2.clone());
        assert_eq!(p.nodes.first().unwrap(), &n1);
        assert_eq!(p.nodes.last().unwrap(), &n2);
        assert_eq!(p.nodes_count(), 2);
        assert_eq!(p.edge_count(), 1);
    }
}