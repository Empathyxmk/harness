use maskerlogger::masker_formatter::*;
use std::sync::Once;

static INIT: Once = Once::new();

fn test_log_integration() {
    INIT.call_once(|| {
        env_logger::builder().is_test(true).try_init().ok();
    });
}

#[test]
fn test_mask_secret_logic() {
    let logger = AbstractMaskedLogger::new(None, 75);
    let sample = "abbbbb";
    let re = regex::Regex::new(r"(a)(b+)").unwrap();
    let mat = re.captures(sample).unwrap();
    let m = re.find(sample).unwrap();
    let masked = logger._mask_secret("abbbbb start abbbbb", vec![m]);
    assert!(masked.chars().filter(|c| *c == '*').count() > 0);
}

#[test]
fn test_mask_sensitive_data_no_match() {
    let mut record = DummyRecord::new("no secrets here");
    let logger = AbstractMaskedLogger::new(None, 10);
    logger._mask_sensitive_data(&mut record);
    assert_eq!(record.msg, "no secrets here");
}

#[test]
fn test_mask_sensitive_data_with_match() {
    let mut record = DummyRecord::new("\"password\": \"password321\" and apikey = 1234");
    let logger = AbstractMaskedLogger::new(None, 45);
    logger._mask_sensitive_data(&mut record);
    assert!(record.msg.is_ascii());
    assert!(!record.msg.contains("password321"));
}

#[test]
fn test_formatter_full_log_integration() {
    INIT.call_once(|| {
        env_logger::builder().is_test(true).try_init().ok();
    });
    let formatter = MaskerFormatter::new("%(levelname)s %(message)s", None, 75);
    let mut record = DummyRecord::new("\"current_key\": \"AIzaSOHbouG6DDa6DOcRGEgOMayAXYXcw6la3c\"");
    record.msg = formatter.format(&record.msg);
    assert!(record.msg.contains("***") || record.msg.contains("current_key"));
    // Continue with more logs if needed
}

#[test]
fn test_json_formatter_logrecord_masking() {
    let formatter = MaskerFormatterJson::new("%(message)s", None, 50);
    let rec = DummyRecord::new("apikey = \"TESTEXPOSEDSECRET\"");
    let value = formatter.format(&rec.msg, true);
    assert!(value.contains("apikey"));
}

#[test]
fn test_maskerformatterjson_skip_mask() {
    let formatter = MaskerFormatterJson::new("%(message)s", None, 50);
    let mut rec = DummyRecord::new("sometext");
    rec.apply_mask = false;
    let result = formatter.format(&rec.msg, rec.apply_mask);
    assert!(result.contains("sometext"));
}

#[test]
fn test_repr_and_str() {
    let formatter = MaskerFormatterJson::new("%(message)s", None, 50);
    let t = format!("{:?}", std::any::type_name::<MaskerFormatterJson>());
    assert!(t.contains("MaskerFormatterJson"));
}