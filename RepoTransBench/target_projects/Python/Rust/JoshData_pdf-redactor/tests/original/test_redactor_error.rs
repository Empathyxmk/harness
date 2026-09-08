use pdf_redactor_rs::pdf_redactor::{RedactorOptions, redactor};

struct DummyStream;
impl DummyStream {
    fn read(&self) -> Vec<u8> {
        b"not a pdf".to_vec()
    }
}

#[test]
fn test_pdf_parse_error() {
    let mut opts = RedactorOptions::default();
    opts.input_stream = Some(DummyStream.read());
    let mut output = vec![];
    let result = redactor(&mut opts, opts.input_stream.clone(), &mut output);

    // Accept any error type, we should get an "Ok" because our stub is forgiving,
    // so we'll simulate the intent by forcing an error
    if result.is_ok() {
        // The dummy implementation does not error by default,
        // so to simulate, we force error when input is exactly "not a pdf"
        let in_bytes = opts.input_stream.as_ref().unwrap();
        if in_bytes == b"not a pdf" {
            panic!("Exception not raised on invalid PDF input");
        }
    }
}