use gvanim::animation::{Step, Animation, ParseException};

#[test]
fn test_step_copy_and_repr() {
    let mut step1 = Step::default();
    step1.V.insert(1);
    step1.E.insert((1, 2));
    step1.lV.insert(1, "A".to_string());
    step1.lE.insert((1, 2), "EdgeLabel".to_string());
    let step2 = Step::from_other(&step1);
    assert_eq!(step2.V, step1.V);
    assert_eq!(step2.E, step1.E);
    assert_eq!(step2.lV, step1.lV);
    assert_eq!(step2.lE, step1.lE);
    let r = format!("{:?}", step2);
    assert!(r.contains("V") && r.contains("E"));
}

#[test]
fn test_node_format_basic() {
    let mut s = Step::default();
    s.V.insert(1);
    s.lV.insert(1, "A".to_string());
    s.hV.insert(1, "blue".to_string());
    let res = s.node_format(1);
    assert!(res.contains("label=") && res.contains("color=blue"));
}

#[test]
fn test_node_format_hidden() {
    let s = Step::default();
    let res = s.node_format(99);
    assert!(res.contains("style=invis"));
}

#[test]
fn test_edge_format_all() {
    let mut s = Step::default();
    let e = (1, 2);
    s.E.insert(e);
    s.lE.insert(e, "lbl".to_string());
    s.hE.insert(e, "green".to_string());
    let res = s.edge_format(e);
    assert!(res.contains("label=") && res.contains("color=green"));
}

#[test]
fn test_edge_format_hidden() {
    let s = Step::default();
    let res = s.edge_format((3, 4));
    assert!(res.contains("style=invis"));
}

#[test]
fn test_animation_action_methods() {
    let mut anim = Animation::default();
    anim.next_step();
    anim.add_node(1);
    anim.highlight_node(2, "yellow");
    anim.label_node(2, "Y");
    anim.unlabel_node(2);
    anim.remove_node(2);
    anim.add_edge(1, 3);
    anim.highlight_edge(1, 3, "green");
    anim.label_edge(1, 3, "E");
    anim.unlabel_edge(1, 3);
    anim.remove_edge(1, 3);
    // No assertion; just check for panics.
}

#[test]
fn test_animation_parse_good() {
    let mut anim = Animation::default();
    let cmds = vec![
        "an 7", "ae 7 8", "ln 7 labelA", "le 7 8 labelE",
        "hn 7", "he 7 8", "ns", "un 7", "ue 7 8", "rn 7", "re 7 8",
    ];
    assert!(anim.parse(cmds).is_ok());
}

#[test]
fn test_animation_parse_bad() {
    let mut anim = Animation::default();
    let cmds = vec!["foobar 1"];
    let res = anim.parse(cmds);
    assert!(res.is_err());
}

#[test]
fn test_animation_parse_bad_format() {
    let mut anim = Animation::default();
    let cmds1 = vec!["ae 2"];
    assert!(anim.parse(cmds1).is_err());
    let cmds2 = vec!["an notanint"];
    assert!(anim.parse(cmds2).is_err());
}