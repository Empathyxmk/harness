#[cfg(test)]
mod tests {
    use super::super::super::src::node::{Node, ParamValue};
    use std::collections::HashMap;

    #[test]
    fn test_to_string() {
        let n = Node::new();
        assert_eq!(n.to_string_repr(), "");
        let n2 = Node::id(1);
        assert_eq!(n2.to_string_repr(), "");
    }
    #[test]
    fn test_comparision() {
        assert_eq!(Node::new(), Node::new());
        assert_eq!(Node::id(1), Node::id(1));
        assert_ne!(Node::id(1), Node::id(2));
        let n1 = Node::id(1);
        let mut n2 = Node::id(1);
        n2.alias = Some("b".into());
        assert_eq!(n1, n2);
    }
}