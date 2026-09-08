use pdf_redactor_rs::pdf_redactor::{RedactorOptions};

#[test]
fn test_options_defaults() {
    let opts = RedactorOptions::default();
    assert_eq!(opts.input_stream, None);
    assert_eq!(opts.output_stream, None);
    assert_eq!(opts.metadata_filters.len(), 0);
    assert_eq!(opts.xmp_filters.len(), 0);
    assert!(opts.xmp_serializer.is_none());
    assert_eq!(opts.content_filters.len(), 0);
    assert_eq!(opts.content_replacement_glyphs, vec!['?', '#', '*', ' ']);
    assert_eq!(opts.link_filters.len(), 0);
}

#[test]
fn test_setting_options() {
    use regex::Regex;
    let mut opts = RedactorOptions::default();
    opts.input_stream = Some(b"input".to_vec());
    opts.output_stream = Some(b"output".as_bytes().to_vec());
    opts.metadata_filters.insert(
        "Title".to_string(),
        vec![Box::new(|_v| Some("NewTitle".to_string()))],
    );
    opts.content_filters = vec![];
    opts.link_filters = vec![Box::new(|_href, _annotation| None)];
    opts.xmp_filters = vec![Box::new(|_xml| None)];
    opts.xmp_serializer = Some(Box::new(|_xml| "<xml />".to_string()));

    assert_eq!(opts.input_stream, Some(b"input".to_vec()));
    assert_eq!(opts.output_stream, Some(b"output".as_bytes().to_vec()));
    assert!(opts.metadata_filters["Title"][0]("test").is_some());
    assert!(opts.link_filters[0]("href", None).is_none());
    assert!(opts.xmp_filters[0]("data").is_none());
    assert_eq!(opts.xmp_serializer.as_ref().unwrap()("ignored"), "<xml />");
}