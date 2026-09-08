use std::collections::HashMap;
use scrapinghub_adblockparser::adblockparser::{AdblockRule, AdblockRules};

#[test]
fn test_simple_matching_public() {
    let rule = AdblockRule::new("ad/");
    assert!(rule.match_url("http://x.com/ad/foo.png", None));
    assert!(!rule.match_url("http://x.com/images/foo.png", None));
}

#[test]
fn test_multiple_rules_public() {
    let rules = vec![
        "foo.js",
        "@@bar.js"
    ];
    let abl = AdblockRules::new(rules);

    assert!(abl.should_block("http://ex.com/blah/foo.js", None));
    assert!(!abl.should_block("http://ex.com/blah/bar.js", None));
}