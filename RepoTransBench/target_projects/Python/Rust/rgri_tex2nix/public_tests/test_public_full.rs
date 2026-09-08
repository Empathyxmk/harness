// Integration test for latex2nix and detect_documentclass public API

use rgri_tex2nix::tex2nix::*;

#[test]
fn test_full_tex2nix_pipeline() {
    let tex_example = r#"
        \documentclass[10pt]{report}
        \usepackage{pdfpages}
        \usepackage{mhchem}
    "#;
    let pkgs = latex2nix(tex_example);
    assert!(pkgs.contains(&"pdfpages".to_string()));
    assert!(pkgs.contains(&"mhchem".to_string()));
    assert_eq!(pkgs.iter().filter(|x| *x == "pdfpages").count(), 1);

    let docclass = detect_documentclass(tex_example);
    assert_eq!(docclass, Some("report".to_string()));
}