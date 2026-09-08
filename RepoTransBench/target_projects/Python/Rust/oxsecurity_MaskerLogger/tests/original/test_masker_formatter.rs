use maskerlogger::masker_formatter::*;

#[test]
fn test_no_masking_if_no_match() {
    let formatter = MaskerFormatter::new("%(message)s", None, 10);
    let rec = DummyRecord::new("nothing secret here");
    let out = formatter.format(&rec.msg);
    assert_eq!(out, "nothing secret here");
}

#[test]
fn test_masking_with_regex_match() {
    let formatter = MaskerFormatter::new("%(message)s", None, 10);
    let rec = DummyRecord::new("password: hunter2");
    let out = formatter.format(&rec.msg);
    assert!(out.contains("***"));
}

#[test]
fn test_skip_mask() {
    let formatter = MaskerFormatterJson::new("%(message)s", None, 10);
    let mut rec = DummyRecord::new("skip masking please");
    rec.apply_mask = false;
    let out = formatter.format(&rec.msg, rec.apply_mask);
    assert_eq!(out, "skip masking please");
}

#[test]
fn test_mask_secret() {
    let logger = AbstractMaskedLogger::new(None, 10);
    let sample = "password: hunter2";
    let re = regex::Regex::new(r"(hunter2)").unwrap();
    let m = re.find(sample).unwrap();
    let masked = logger._mask_secret("password: hunter2", vec![m]);
    assert!(masked.contains("***"));
}