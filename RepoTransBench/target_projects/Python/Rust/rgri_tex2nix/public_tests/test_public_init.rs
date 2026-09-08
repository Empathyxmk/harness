use rgri_tex2nix::tex2nix::*;

fn get_version() -> Option<String> {
    Some(version().to_string())
}

#[test]
fn test_tex2nix_version() {
    let version = get_version();
    if let Some(ver) = version {
        assert!(ver.chars().all(|c| c.is_digit(10) || c == '.'));
        assert_eq!(ver.split('.').count(), 3);
    }
}

#[test]
fn test_latex2nix_example_usage() {
    let input_tex = r#"
        \documentclass{scrreprt}
        \usepackage{fancyhdr}
        \usepackage{longtable}
        \begin{document}
        LaTeX public sample!
        \end{document}
    "#;
    let pkgs = latex2nix(input_tex);
    assert!(pkgs.contains(&"fancyhdr".to_string()));
    assert!(pkgs.contains(&"longtable".to_string()));
    assert!(!pkgs.contains(&"geometry".to_string()));
}

#[test]
fn test_latex2nix_handles_empty() {
    let pkgs = latex2nix("");
    assert!(pkgs.is_empty());
}

#[test]
fn test_latex2nix_no_duplicates() {
    let input_tex = r#"
        \usepackage{todonotes}
        \usepackage{todonotes}
        \usepackage{colortbl}
    "#;
    let pkgs = latex2nix(input_tex);
    assert_eq!(pkgs.iter().filter(|x| *x == "todonotes").count(), 1);
    assert_eq!(pkgs.iter().filter(|x| *x == "colortbl").count(), 1);
}

#[test]
fn test_latex2nix_custom_package() {
    let input_tex = r#"
        \documentclass{standalone}
        \usepackage{publicpackage}
        \begin{document}
        Public
        \end{document}
    "#;
    let pkgs = latex2nix(input_tex);
    assert!(pkgs.contains(&"publicpackage".to_string()));
}

#[test]
fn test_latex2nix_multiline_usepackage() {
    let input_tex = r#"
        \usepackage{pgfplots,
        subcaption,
        caption}
    "#;
    let pkgs = latex2nix(input_tex);
    for p in &["pgfplots", "subcaption", "caption"] {
        assert!(pkgs.contains(&p.to_string()));
    }
}

#[test]
fn test_latex2nix_with_comment_lines() {
    let input_tex = r#"
        % Just a comment line
        \usepackage{blindtext}
        % trailing comment
    "#;
    let pkgs = latex2nix(input_tex);
    assert!(pkgs.contains(&"blindtext".to_string()));
}

#[test]
fn test_latex2nix_optional_arg() {
    let input_tex = r#"
        \usepackage[top=2cm]{geometry}
        \usepackage[usenames]{color}
    "#;
    let pkgs = latex2nix(input_tex);
    assert!(pkgs.contains(&"geometry".to_string()));
    assert!(pkgs.contains(&"color".to_string()));
}

#[test]
fn test_latex2nix_ignores_unrelated_lines() {
    let input_tex = r#"
        123 random text line
        \date{}
    "#;
    let pkgs = latex2nix(input_tex);
    assert!(pkgs.is_empty());
}

#[test]
fn test_detect_documentclass() {
    let input_tex = r#"
        \documentclass{memoir}
        \usepackage{zref}
    "#;
    let docclass = detect_documentclass(input_tex);
    assert_eq!(docclass, Some("memoir".to_string()));
}

#[test]
fn test_detect_documentclass_none() {
    let input_tex = r#"
        % no docclass here
        \usepackage{moreverb}
    "#;
    let docclass = detect_documentclass(input_tex);
    assert_eq!(docclass, None);
}