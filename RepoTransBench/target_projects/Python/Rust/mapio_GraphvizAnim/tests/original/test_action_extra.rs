use gvanim::action;
use gvanim::animation::Step;

#[test]
fn test_add_node_action() {
    let mut s = vec![Step::default()];
    action::AddNode(42).call(&mut s);
    assert!(s.last().unwrap().V.contains(&42));
}

#[test]
fn test_highlight_node_and_label_node() {
    let mut s = vec![Step::default()];
    action::HighlightNode { node: 2, color: "blue".to_string() }.call(&mut s);
    action::LabelNode { node: 2, label: "lbl".to_string() }.call(&mut s);
    let st = s.last().unwrap();
    assert!(st.hV.contains_key(&2) && st.lV.contains_key(&2));
}

#[test]
fn test_unlabel_and_remove_node() {
    let mut s = vec![Step::default()];
    action::AddNode(1).call(&mut s);
    action::LabelNode { node: 1, label: "tok".to_string() }.call(&mut s);
    action::UnlabelNode(1).call(&mut s);
    assert!(!s.last().unwrap().lV.contains_key(&1));
    action::RemoveNode(1).call(&mut s);
    assert!(!s.last().unwrap().V.contains(&1));
}

#[test]
fn test_add_edge_and_highlight_label_unlabel_remove() {
    let mut s = vec![Step::default()];
    action::AddNode(3).call(&mut s);
    action::AddNode(4).call(&mut s);
    action::AddEdge(3, 4).call(&mut s);
    action::HighlightEdge { n1: 3, n2: 4, color: "green".to_string() }.call(&mut s);
    action::LabelEdge { n1: 3, n2: 4, label: "X".to_string() }.call(&mut s);

    let st = s.last().unwrap();
    assert!(st.E.contains(&(3, 4)) && st.hE.contains_key(&(3, 4)) && st.lE.contains_key(&(3, 4)));
    action::UnlabelEdge(3, 4).call(&mut s);
    action::RemoveEdge(3, 4).call(&mut s);
    assert!(!s.last().unwrap().E.contains(&(3, 4)));
}