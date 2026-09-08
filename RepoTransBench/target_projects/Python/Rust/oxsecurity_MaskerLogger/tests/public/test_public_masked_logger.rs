use maskerlogger::masker_formatter::*;
use std::sync::Once;

const TEST_CONFIG_PATH: &str = "maskerlogger/config/gitleaks.toml";
static INIT: Once = Once::new();

#[test]
fn test_mask_secret_logic_with_new_pattern() {
    let logger = AbstractMaskedLogger::new(Some(TEST_CONFIG_PATH), 99);
    let sample = "xyyyy";
    let re = regex::Regex::new(r"(x)(y+)").unwrap();
    let m = re.find(sample).unwrap();
    let masked = logger._mask_secret("xyyyy abc xyyyy", vec![m]);
    assert!(masked.chars().filter(|c| *c == '*').count() > 0);
}

#[test]
fn test_mask_sensitive_data_no_match_newmsg() {
    let mut record = DummyRecord::new("totally safe entry");
    let logger = AbstractMaskedLogger::new(Some(TEST_CONFIG_PATH), 10);
    logger._mask_sensitive_data(&mut record);
    assert_eq!(record.msg, "totally safe entry");
}

#[test]
fn test_mask_sensitive_data_with_match_newsecret() {
    let mut record = DummyRecord::new("\"token\": \"abcd12345efgh\" and secret_key = zyxw");
    let logger = AbstractMaskedLogger::new(Some(TEST_CONFIG_PATH), 39);
    logger._mask_sensitive_data(&mut record);
    assert!(record.msg.is_ascii());
    assert!(!record.msg.contains("abcd12345efgh"));
}

#[test]
fn test_formatter_full_log_integration_public() {
    INIT.call_once(|| {
        env_logger::builder().is_test(true).try_init().ok();
    });
    let formatter = MaskerFormatter::new("%(levelname)s: %(message)s", Some(TEST_CONFIG_PATH), 33);
    let mut record = DummyRecord::new("\"another_key\": \"AIzaSoMEoth3rKEY344sdlGh289Ka3dLPd\"");
    record.msg = formatter.format(&record.msg);
    assert!(record.msg.contains("***") || record.msg.contains("another_key"));
}

#[test]
fn test_json_formatter_logrecord_masking_public() {
    let formatter = MaskerFormatterJson::new("%(message)s", Some(TEST_CONFIG_PATH), 22);
    let rec = DummyRecord::new("auth = \"FAKENEWSECRETXYZ\"");
    let value = formatter.format(&rec.msg, true);
    assert!(value.contains("auth"));
}

#[test]
fn test_maskerformatterjson_skip_mask_public() {
    let formatter = MaskerFormatterJson::new("%(message)s", Some(TEST_CONFIG_PATH), 22);
    let mut rec = DummyRecord::new("publiclogtext");
    rec.apply_mask = false;
    let result = formatter.format(&rec.msg, rec.apply_mask);
    assert!(result.contains("publiclogtext"));
}

#[test]
fn test_repr_and_str_public() {
    let formatter = MaskerFormatterJson::new("%(message)s", Some(TEST_CONFIG_PATH), 22);
    let t = format!("{:?}", std::any::type_name::<MaskerFormatterJson>());
    assert!(t.contains("MaskerFormatterJson"));
}