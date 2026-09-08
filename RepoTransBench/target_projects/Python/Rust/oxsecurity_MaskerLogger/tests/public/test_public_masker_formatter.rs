use maskerlogger::masker_formatter::*;

#[test]
fn test_no_masking_if_no_match_public() {
    let formatter = MaskerFormatter::new("%(message)s", None, 10);
    let rec = DummyRecord::new("12345 is a safe message");
    let out = formatter.format(&rec.msg);
    assert_eq!(out, "12345 is a safe message");
}

#[test]
fn test_masking_with_regex_match_public() {
    let formatter = MaskerFormatter::new("%(message)s", None, 10);
    let rec = DummyRecord::new("apikey: mytopsecret");
    let out = formatter.format(&rec.msg);
    assert!(out.contains("***"));
}

#[test]
fn test_skip_mask_public() {
    let formatter = MaskerFormatterJson::new("%(message)s", None, 10);
    let mut rec = DummyRecord::new("nothing to mask here");
    rec.apply_mask = false;
    let out = formatter.format(&rec.msg, rec.apply_mask);
    assert_eq!(out, "nothing to mask here");
}

#[test]
fn test_mask_secret_public() {
    let logger = AbstractMaskedLogger::new(None, 10);
    let sample = "apikey: mytopsecret";
    let re = regex::Regex::new(r"(mytopsecret)").unwrap();
    let m = re.find(sample).unwrap();
    let masked = logger._mask_secret("apikey: mytopsecret", vec![m]);
    assert!(masked.contains("***"));
}