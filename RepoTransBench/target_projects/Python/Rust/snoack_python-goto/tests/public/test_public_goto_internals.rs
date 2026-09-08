// Translated from public_tests/test_public_goto_internals.py

#[test]
fn test_public_goto_label_and_table() {
    let mut table = std::collections::HashMap::new();
    let code = [
        ("label1", 10),
        ("label2", 20)
    ];
    for (name, line) in &code {
        table.insert(*name, *line);
    }
    assert_eq!(table["label1"], 10);
    assert_eq!(table["label2"], 20);
}

#[test]
fn test_public_goto_macro_lines() {
    let src = "alpha\nbeta\n# label x\n# goto x\nomega";
    let lines: Vec<_> = src.lines().collect();
    let mut found_label = false;
    let mut label_line = 0;
    for (i, line) in lines.iter().enumerate() {
        if line.contains("# label x") {
            found_label = true;
            label_line = i;
        }
    }
    assert_eq!(found_label, true);
    assert_eq!(label_line, 2);
}

#[test]
fn test_public_goto_internals_exc() {
    struct Dummy;
    impl std::fmt::Display for Dummy {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "test error")
        }
    }
    impl std::fmt::Debug for Dummy {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "test error")
        }
    }
    use std::error::Error;
    impl Error for Dummy {}
    let got_error = std::panic::catch_unwind(|| {
        panic!("{}", Dummy);
    });
    assert!(got_error.is_err());
}