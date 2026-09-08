#[cfg(test)]
mod tests {
    use super::super::super::src::edge::Edge;
    use super::super::super::src::node::{Node, ParamValue};
    use std::collections::HashMap;

    #[test]
    fn test_init() {
        let n1 = Node::new();
        let n2 = Node::new();
        let mut props = HashMap::new();
        props.insert("a".to_string(), ParamValue::S("a".to_string()));
        props.insert("b".to_string(), ParamValue::I(10));
        let _e = Edge::with_props(n1.clone(), None, n2.clone(), props);

        // Minimal negative tests
        let _ = Edge::new(n1.clone(), None, n2.clone());
    }

    #[test]
    fn test_to_string() {
        let n1 = Node::new();
        let n2 = Node::new();
        let mut props = HashMap::new();
        props.insert("a".to_string(), ParamValue::S("a".to_string()));
        props.insert("b".to_string(), ParamValue::I(10));
        let e = Edge::with_props(n1.clone(), None, n2.clone(), props);
        let _ = e.to_string_repr();
        let e2 = Edge::with_props(n1.clone(), None, n2.clone(), HashMap::new());
        let _ = e2.to_string_repr();
    }

    #[test]
    fn test_comparision() {
        let n1 = Node::id(1);
        let n2 = Node::id(2);
        let n3 = Node::id(3);
        let e1 = Edge::new(n1.clone(), None, n2.clone());
        assert_eq!(e1, Edge::new(n1.clone(), None, n2.clone()));
        assert_ne!(e1, Edge::new(n1.clone(), Some("bla".into()), n2.clone()));
        assert_ne!(e1, Edge::new(n1.clone(), None, n3.clone()));
        assert_ne!(e1, Edge::new(n3.clone(), None, n2.clone()));
        assert_ne!(e1, Edge::new(n2.clone(), None, n1.clone()));
        let mut props = HashMap::new();
        props.insert("a".to_string(), ParamValue::I(10));
        assert_ne!(e1, Edge::with_props(n1.clone(), None, n2.clone(), props));
    }
}