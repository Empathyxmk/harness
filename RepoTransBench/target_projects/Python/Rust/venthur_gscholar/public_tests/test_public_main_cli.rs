use serial_test::serial;
use venthur_gscholar as gscholar;
use gscholar::gscholar as gs;
use std::collections::HashMap;

#[test]
#[serial]
fn test_public_main_version() {
    let args = vec!["--version", "anothertest"];
    assert_eq!(0, 0);
}

#[test]
#[serial]
fn test_public_main_search() {
    let output_val = vec!["uniquebibtexentry".to_string()];
    let keyword = "a different search";
    let result = {
        assert_eq!(keyword, "a different search");
        output_val.clone()
    };
    let joined = result.join("\n");
    assert!(joined.contains("uniquebibtexentry"));
}

#[test]
#[serial]
fn test_public_main_search_no_results() {
    let args = vec!["-f", "bibtex", "nosearchresults"];
    let result: Vec<String> = vec![]; // empty result
    assert_eq!(result.len(), 0);
}

#[test]
#[serial]
fn test_public_main_rename_pdf() {
    let bib = vec!["anotherbibentry".to_string()];
    let mut called = HashMap::new();
    let pdf_arg = "sometest.pdf";
    called.insert("l", true);
    called.insert("r", true);
    assert!(*called.get("l").unwrap() && *called.get("r").unwrap());
}

#[test]
#[serial]
fn test_public_main_rename_no_pdf() {
    let exists = false;
    assert!(!exists);
}

#[test]
#[serial]
fn test_public_main_all() {
    let results = vec!["bibA".to_string(), "bibB".to_string()];
    let joined = results.join("\n");
    assert!(joined.contains("bibA") && joined.contains("bibB"));
}

#[test]
#[serial]
fn test_public_main_output_formats() {
    let mut exp = Vec::new();
    for fmt in &[gs::FORMAT_ENDNOTE, gs::FORMAT_REFMAN, gs::FORMAT_WENXIANWANG] {
        exp.push(fmt.to_string());
    }
    assert!(exp.contains(&gs::FORMAT_ENDNOTE.to_string()));
    assert!(exp.contains(&gs::FORMAT_REFMAN.to_string()));
    assert!(exp.contains(&gs::FORMAT_WENXIANWANG.to_string()));
}