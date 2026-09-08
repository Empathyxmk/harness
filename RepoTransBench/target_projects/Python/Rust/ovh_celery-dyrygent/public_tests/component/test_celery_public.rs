use crate::celery::entities::{Signature, Chord, Chain, Group};
use std::collections::HashMap;

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn test_signature_public() {
        let mut k = HashMap::new();
        k.insert("k".to_string(), json!(7));
        let mut sig = Signature::new("test_func", vec![json!(9), json!(8)], k.clone());
        assert_eq!(sig.name, "test_func");
        assert_eq!(sig.args, vec![json!(9), json!(8)]);
        assert_eq!(sig.kwargs.get("k"), Some(&json!(7)));
    }

    #[test]
    fn test_chord_public() {
        let sig_a = Signature::new("sigA", vec![json!(1)], HashMap::new());
        let body = Signature::new("bodyA", vec![], HashMap::new());
        let chord = Chord::new(vec![sig_a.clone()], body.clone());
        assert_eq!(chord.header[0].name, "sigA");
        assert_eq!(chord.body.name, "bodyA");
    }

    #[test]
    fn test_chain_and_group_public() {
        let c = Chain::new(vec![Signature::new("z", vec![], HashMap::new())]);
        let g = Group::new(vec![
            Signature::new("a", vec![], HashMap::new()),
            Signature::new("b", vec![json!(1)], HashMap::new())
        ]);
        assert_eq!(c.tasks.len(), 1);
        assert_eq!(g.tasks.len(), 2);
    }
}