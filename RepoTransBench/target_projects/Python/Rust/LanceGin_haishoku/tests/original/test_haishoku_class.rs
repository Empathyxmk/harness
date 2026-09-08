use haishoku_rs::haishoku::Haishoku;

#[test]
fn test_haishoku_init_sets_none() {
    let h = Haishoku::new();
    assert!(h.dominant.is_none());
    assert!(h.palette.is_none());
}

#[test]
fn test_load_haishoku_monkeypatch() {
    // In Rust we cannot monkeypatch, so use from_path API to simulate patched values
    let h = Haishoku::from_path("fake/path.png");
    assert_eq!(h.palette, Some(vec![(200,100,50); 6]));
    assert_eq!(h.dominant, Some(("dom".to_owned(), (0, 0, 0))));
}

#[test]
fn test_load_haishoku_is_callable() {
    // In Rust, method reference is callable
    let f: fn(&str) -> &Haishoku = Haishoku::load_haishoku;
    let _ = f;
}

#[test]
fn test_str_repr_of_haishoku() {
    let h = Haishoku::default();
    let s = format!("{}", h);
    let r = format!("{:?}", h);
    assert!(!s.is_empty());
    assert!(!r.is_empty());
}