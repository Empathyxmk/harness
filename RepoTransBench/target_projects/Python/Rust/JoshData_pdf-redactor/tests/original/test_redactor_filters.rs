use pdf_redactor_rs::pdf_redactor::{RedactorOptions, redactor};
use regex::Regex;
use std::collections::HashMap;

#[derive(Default)]
struct DummyPdf {
    pub info: HashMap<String, String>,
}
fn dummy_pdf_reader(_stream: &[u8]) -> DummyPdf {
    DummyPdf { info: HashMap::new() }
}
fn dummy_pdf_writer(_doc: &DummyPdf, _stream: &mut Vec<u8>) {}

struct DummyOptions {
    pub redactor_opts: RedactorOptions,
}
impl DummyOptions {
    pub fn new() -> Self {
        DummyOptions {
            redactor_opts: RedactorOptions::default(),
        }
    }
}

#[test]
fn test_metadata_update() {
    let mut opts = RedactorOptions::default();
    opts.input_stream = Some(b"%PDF-1.4 mock pdf".to_vec());
    opts.output_stream = Some(vec![]);
    opts.metadata_filters.insert(
        "Title".to_string(),
        vec![Box::new(|_v| Some("UPPER".to_string()))],
    );
    opts.metadata_filters
        .insert("DEFAULT".to_string(), vec![Box::new(|_v| None)]);
    let mut output = vec![];
    let _ = redactor(&mut opts, opts.input_stream.clone(), &mut output);
    // Test only that logic executes and doesn't panic
}

#[test]
fn test_content_filter() {
    let mut opts = RedactorOptions::default();
    opts.input_stream = Some(b"%PDF-1.4...".to_vec());
    opts.output_stream = Some(vec![]);
    opts.content_filters = vec![(Regex::new("foo").unwrap(), Box::new(|_m| "bar".to_string()))];
    let mut output = vec![];
    let _ = redactor(&mut opts, opts.input_stream.clone(), &mut output);
    // Test only that logic executes and doesn't panic
}