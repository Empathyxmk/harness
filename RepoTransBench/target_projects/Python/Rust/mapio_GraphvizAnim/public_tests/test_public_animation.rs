use gvanim::animation::{Step, Animation, ParseException};

#[test]
fn test_step_copy_and_repr_public() {
    let mut step1 = Step::default();
    step1.V.insert(10);
    step1.E.insert((10, 20));
    step1.lV.insert(10, "X".to_string());
    step1.lE.insert((10, 20), "EdgeAB".to_string());
    let step2 = Step::from_other(&step1);
    assert_eq!(step2.V, step1.V);
    assert_eq!(step2.E, step1.E);
    assert_eq!(step2.lV, step1.lV);
    assert_eq!(step2.lE, step1.lE);
    let r = format!("{:?}", step2);
    assert!(r.contains("V") && r.contains("E"));
}

#[test]
fn test_node_format_basic_public() {
    let mut s = Step::default();
    s.V.insert(5);
    s.lV.insert(5, "B".to_string());
    s.hV.insert(5, "red".to_string());
    let res = s.node_format(5);
    assert!(res.contains("label=") && res.contains("color=red"));
}

#[test]
fn test_node_format_hidden_public() {
    let s = Step::default();
    let res = s.node_format(123);
    assert!(res.contains("style=invis"));
}

#[test]
fn test_edge_format_all_public() {
    let mut s = Step::default();
    let e = (7, 8);
    s.E.insert(e);
    s.lE.insert(e, "labelZ".to_string());
    s.hE.insert(e, "orange".to_string());
    let res = s.edge_format(e);
    assert!(res.contains("label=") && res.contains("color=orange"));
}

#[test]
fn test_edge_format_hidden_public() {
    let s = Step::default();
    let res = s.edge_format((17, 28));
    assert!(res.contains("style=invis"));
}

#[test]
fn test_animation_action_methods_public() {
    let mut anim = Animation::default();
    anim.next_step();
    anim.add_node(101);
    anim.highlight_node(201, "purple");
    anim.label_node(201, "Z");
    anim.unlabel_node(201);
    anim.remove_node(201);
    anim.add_edge(101, 301);
    anim.highlight_edge(101, 301, "pink");
    anim.label_edge(101, 301, "F");
    anim.unlabel_edge(101, 301);
    anim.remove_edge(101, 301);
}

#[test]
fn test_animation_parse_good_public() {
    let mut anim = Animation::default();
    let cmds = vec![
        "an 17", "ae 17 18", "ln 17 labelB", "le 17 18 labelF",
        "hn 17", "he 17 18", "ns", "un 17", "ue 17 18", "rn 17", "re 17 18",
    ];
    assert!(anim.parse(cmds).is_ok());
}

#[test]
fn test_animation_parse_bad_public() {
    let mut anim = Animation::default();
    let cmds = vec!["badcmd 77"];
    assert!(anim.parse(cmds).is_err());
}

#[test]
fn test_animation_parse_bad_format_public() {
    let mut anim = Animation::default();
    let cmds1 = vec!["ae"];
    assert!(anim.parse(cmds1).is_err());
    let cmds2 = vec!["an invalidnum"];
    assert!(anim.parse(cmds2).is_err());
}