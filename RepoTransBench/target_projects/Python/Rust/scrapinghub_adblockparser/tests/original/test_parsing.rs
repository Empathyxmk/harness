use std::collections::HashMap;
use scrapinghub_adblockparser::adblockparser::{AdblockRule, AdblockRules};

#[test]
fn test_rule_simple() {
    let rule = AdblockRule::new("banner/");
    assert!(rule.match_url("http://example.com/banner/ad.gif", None));
    assert!(!rule.match_url("http://example.com/ads/ad.gif", None));
}

#[test]
fn test_rule_with_options() {
    let rule = AdblockRule::new("ad.js$script");
    let mut params = HashMap::new();
    params.insert("script".to_string(), "1".to_string());
    assert!(rule.match_url("http://example.com/js/ad.js", Some(&params)));

    params.clear();
    params.insert("image".to_string(), "1".to_string());
    assert!(!rule.match_url("http://example.com/js/ad.js", Some(&params)));
}

#[test]
fn test_should_block() {
    let rules = vec![
        "ad.js",
        "banner/",
        "@@good.js"
    ];
    let abl = AdblockRules::new(rules);
    let mut params = HashMap::new();

    assert!(abl.should_block("http://example.com/ad.js", None));
    assert!(abl.should_block("http://example.com/banner/123.png", None));
    assert!(!abl.should_block("http://example.com/good.js", None));
}

#[test]
fn test_exception_rule() {
    let rules = vec![
        "ad.js",
        "@@/goodad/"
    ];
    let abl = AdblockRules::new(rules);
    assert!(!abl.should_block("http://example.com/goodad/ad.js", None));
    assert!(abl.should_block("http://example.com/evilad/ad.js", None));
}