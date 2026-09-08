use zaproxy_zap_api_rust::zapv2::rule_config::{DummyZapRuleConfig, RuleConfig};

fn setup_ruleconfig<'a>() -> RuleConfig<'a> {
    let mut zap = Box::new(DummyZapRuleConfig::new());
    RuleConfig::new(Box::leak(zap))
}

#[test]
fn test_rule_config_value() {
    let mut ruleconfig = setup_ruleconfig();
    let r = ruleconfig.rule_config_value("key1");
    assert_eq!(r, "dummy");
}

#[test]
fn test_all_rule_configs() {
    let mut ruleconfig = setup_ruleconfig();
    let v = ruleconfig.all_rule_configs();
    assert_eq!(v, "dummy");
}

#[test]
fn test_reset_rule_config_value() {
    let mut ruleconfig = setup_ruleconfig();
    let v = ruleconfig.reset_rule_config_value("key2");
    assert_eq!(v, "dummy");
}

#[test]
fn test_reset_all_rule_config_values() {
    let mut ruleconfig = setup_ruleconfig();
    let v = ruleconfig.reset_all_rule_config_values();
    assert_eq!(v, "dummy");
}

#[test]
fn test_set_rule_config_value_without_value() {
    let mut ruleconfig = setup_ruleconfig();
    let v = ruleconfig.set_rule_config_value("key3", None);
    assert_eq!(v, "dummy");
}

#[test]
fn test_set_rule_config_value_with_value() {
    let mut ruleconfig = setup_ruleconfig();
    let v = ruleconfig.set_rule_config_value("key4", Some("somevalue"));
    assert_eq!(v, "dummy");
}