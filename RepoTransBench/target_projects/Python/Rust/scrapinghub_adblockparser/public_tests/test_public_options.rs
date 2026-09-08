use std::collections::HashMap;
use scrapinghub_adblockparser::adblockparser::AdblockRule;

#[test]
fn test_domain_option_public() {
    let rule = AdblockRule::new("ads$domain=foo.com|~bar.com");
    let mut params = HashMap::new();
    params.insert("domain".to_string(), "foo.com".to_string());
    assert!(rule.match_url("http://foo.com/ads", Some(&params)));

    params.insert("domain".to_string(), "bar.com".to_string());
    assert!(!rule.match_url("http://bar.com/ads", Some(&params)));

    params.insert("domain".to_string(), "baz.com".to_string());
    assert!(!rule.match_url("http://baz.com/ads", Some(&params)));
}