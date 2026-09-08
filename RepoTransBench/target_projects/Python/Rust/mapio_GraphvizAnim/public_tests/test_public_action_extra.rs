use gvanim::action;
use gvanim::animation::Step;

#[test]
fn test_add_node_action_public() {
    let mut s = vec![Step::default()];
    action::AddNode(12).call(&mut s);
    assert!(s.last().unwrap().V.contains(&12));
}

#[test]
fn test_highlight_node_and_label_node_public() {
    let mut s = vec![Step::default()];
    action::HighlightNode { node: 20, color: "red".to_string() }.call(&mut s);
    action::LabelNode { node: 20, label: "lbl2".to_string() }.call(&mut s);
    let st = s.last().unwrap();
    assert!(st.hV.contains_key(&20) && st.lV.contains_key(&20));
}

#[test]
fn test_unlabel_and_remove_node_public() {
    let mut s = vec![Step::default()];
    action::AddNode(9).call(&mut s);
    action::LabelNode { node: 9, label: "zzz".to_string() }.call(&mut s);
    action::UnlabelNode(9).call(&mut s);
    assert!(!s.last().unwrap().lV.contains_key(&9));
    action::RemoveNode(9).call(&mut s);
    assert!(!s.last().unwrap().V.contains(&9));
}

#[test]
fn test_add_edge_and_highlight_label_unlabel_remove_public() {
    let mut s = vec![Step::default()];
    action::AddNode(6).call(&mut s);
    action::AddNode(13).call(&mut s);
    action::AddEdge(6, 13).call(&mut s);
    action::HighlightEdge { n1: 6, n2: 13, color: "purple".to_string() }.call(&mut s);
    action::LabelEdge { n1: 6, n2: 13, label: "Y".to_string() }.call(&mut s);

    let st = s.last().unwrap();
    assert!(st.E.contains(&(6, 13)) && st.hE.contains_key(&(6, 13)) && st.lE.contains_key(&(6, 13)));
    action::UnlabelEdge(6, 13).call(&mut s);
    action::RemoveEdge(6, 13).call(&mut s);
    assert!(!s.last().unwrap().E.contains(&(6, 13)));
}