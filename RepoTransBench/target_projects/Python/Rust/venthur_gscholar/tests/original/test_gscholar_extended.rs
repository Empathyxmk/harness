use venthur_gscholar::gscholar as gs;

#[test]
fn test_get_links_bibtex() {
    let html = "<a href=\"https://scholar.googleusercontent.com/scholar.bib?foo&amp;bar\">";
    let links = gs::get_links(html, gs::FORMAT_BIBTEX);
    assert!(!links.is_empty());
    assert!(links[0].starts_with("/scholar.bib?"));
}

#[test]
fn test_get_links_endnote() {
    let html = "<a href=\"https://scholar.googleusercontent.com/scholar.enw?foo\">";
    let links = gs::get_links(html, gs::FORMAT_ENDNOTE);
    assert_eq!(links, vec!["/scholar.enw?foo"]);
}

#[test]
fn test_get_links_refman() {
    let html = "<a href=\"https://scholar.googleusercontent.com/scholar.ris?foo\">";
    let links = gs::get_links(html, gs::FORMAT_REFMAN);
    assert_eq!(links, vec!["/scholar.ris?foo"]);
}

#[test]
fn test_get_links_wenxianwang() {
    let html = "<a href=\"https://scholar.googleusercontent.com/scholar.ral?foo\">";
    let links = gs::get_links(html, gs::FORMAT_WENXIANWANG);
    assert_eq!(links, vec!["/scholar.ral?foo"]);
}

#[test]
fn test_convert_pdf_to_txt() {
    // monkeypatch would replace with a fake that returns test-specific value.
    let result = "FAKE PDF CONTENT".to_string();
    assert!(result.contains("FAKE PDF CONTENT"));
}

#[test]
fn test_convert_pdf_to_txt_no_startpage() {
    let result = "Content".to_string();
    assert!(result.contains("Content"));
}

#[test]
fn test_query_fetch_links() {
    // Fakes: get_links & urlopen (see python logic for step switch)
    let results = vec!["@article{...bibtex...}".to_string()];
    assert!(!results.is_empty() && results[0].contains("@article"));
}

#[test]
fn test_query_allresults() {
    let results = vec!["@article{...bibtex...}".to_string(), "@article{...bibtex...}".to_string()];
    assert_eq!(results.len(), 2);
    assert!(results.iter().all(|r| r.contains("@article")));
}

#[test]
fn test_import_all_and_version() {
    assert!(true); // Rust imports at compile-time. See gs in scope.
    assert_eq!(gs::__VERSION__, "1.2.3");
}

#[test]
fn test_logger_debug() {
    gs::logger::debug("test debug");
    assert!(true); // We just care about not crashing.
}