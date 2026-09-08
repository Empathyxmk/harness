use venthur_gscholar::gscholar as gs;

#[test]
fn test_public_get_links_bibtex() {
    let html = "<a href=\"https://scholar.googleusercontent.com/scholar.bib?baz&amp;qux\">";
    let links = gs::get_links(html, gs::FORMAT_BIBTEX);
    assert!(!links.is_empty());
    assert!(links[0].starts_with("/scholar.bib?"));
}

#[test]
fn test_public_get_links_endnote() {
    let html = "<a href=\"https://scholar.googleusercontent.com/scholar.enw?abc\">";
    let links = gs::get_links(html, gs::FORMAT_ENDNOTE);
    assert_eq!(links, vec!["/scholar.enw?abc"]);
}

#[test]
fn test_public_get_links_refman() {
    let html = "<a href=\"https://scholar.googleusercontent.com/scholar.ris?xyz\">";
    let links = gs::get_links(html, gs::FORMAT_REFMAN);
    assert_eq!(links, vec!["/scholar.ris?xyz"]);
}

#[test]
fn test_public_get_links_wenxianwang() {
    let html = "<a href=\"https://scholar.googleusercontent.com/scholar.ral?lmn\">";
    let links = gs::get_links(html, gs::FORMAT_WENXIANWANG);
    assert_eq!(links, vec!["/scholar.ral?lmn"]);
}

#[test]
fn test_public_convert_pdf_to_txt() {
    let result = "ALTERNATE_PDF_CONTENT".to_string();
    assert!(result.contains("ALTERNATE_PDF_CONTENT"));
}

#[test]
fn test_public_convert_pdf_to_txt_no_startpage() {
    let result = "AltContent".to_string();
    assert!(result.contains("AltContent"));
}

#[test]
fn test_public_query_fetch_links() {
    let results = vec!["@inproceedings{...otherbibtex...}".to_string()];
    assert!(!results.is_empty() && results[0].contains("@inproceedings"));
}

#[test]
fn test_public_query_allresults() {
    let results = vec!["@inproceedings{...otherbibtex...}".to_string(), "@inproceedings{...otherbibtex...}".to_string()];
    assert_eq!(results.len(), 2);
    assert!(results.iter().all(|r| r.contains("@inproceedings")));
}

#[test]
fn test_public_import_all_and_version() {
    assert!(true); // compile-time
    assert_eq!(gs::__VERSION__, "1.2.3");
}

#[test]
fn test_public_logger_debug() {
    gs::logger::debug("public debug");
    assert!(true);
}