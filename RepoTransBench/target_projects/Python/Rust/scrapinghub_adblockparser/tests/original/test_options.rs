use std::collections::HashMap;
use scrapinghub_adblockparser::adblockparser::{AdblockRule, AdblockRules};

#[test]
fn test_domain_option() {
    // +foo.com|~bar.com|~baz.com
    // means this rule should apply only to foo.com, not to bar.com or baz.com
    let rule = AdblockRule::new("banner/*$domain=foo.com|~bar.com|~baz.com");
    let mut params = HashMap::new();
    params.insert("domain".to_string(), "foo.com".to_string());
    assert!(rule.match_url("http://example.com/banner/ad.gif", Some(&params)));

    params.insert("domain".to_string(), "subdomain.foo.com".to_string());
    assert!(rule.match_url("http://example.com/banner/ad.gif", Some(&params)));

    params.insert("domain".to_string(), "bar.com".to_string());
    assert!(!rule.match_url("http://example.com/banner/ad.gif", Some(&params)));

    params.insert("domain".to_string(), "baz.com".to_string());
    assert!(!rule.match_url("http://example.com/banner/ad.gif", Some(&params)));

    params.insert("domain".to_string(), "other.com".to_string());
    assert!(!rule.match_url("http://example.com/banner/ad.gif", Some(&params)));

    // When domain param is missing, rule should not match
    assert!(!rule.match_url("http://example.com/banner/ad.gif", None));
}

#[test]
fn test_script_option() {
    let rule = AdblockRule::new("ads.js$script,image");
    let mut params = HashMap::new();

    // Should only match script or image
    params.insert("script".to_string(), "1".to_string());
    assert!(rule.match_url("http://ads.com/ads.js", Some(&params)));

    params.clear();
    params.insert("image".to_string(), "1".to_string());
    assert!(rule.match_url("http://ads.com/ads.js", Some(&params)));

    params.clear();
    params.insert("stylesheet".to_string(), "1".to_string());
    assert!(!rule.match_url("http://ads.com/ads.js", Some(&params)));

    params.clear();
    assert!(!rule.match_url("http://ads.com/ads.js", Some(&params)));
}

#[test]
fn test_not_script_option() {
    let rule = AdblockRule::new("ads.js$~script");
    let mut params = HashMap::new();

    params.insert("script".to_string(), "1".to_string());
    assert!(!rule.match_url("http://ads.com/ads.js", Some(&params)), "Should not match scripts");

    params.clear();
    params.insert("image".to_string(), "1".to_string());
    assert!(rule.match_url("http://ads.com/ads.js", Some(&params)), "Should match non-scripts");

    params.clear();
    assert!(rule.match_url("http://ads.com/ads.js", Some(&params)), "Should match with no type param");
}

#[test]
fn test_multiple_params() {
    let rule = AdblockRule::new("foo$script,third-party,domain=foo.com|bar.com");
    let mut params = HashMap::new();

    params.insert("script".to_string(), "1".to_string());
    params.insert("third-party".to_string(), "1".to_string());
    params.insert("domain".to_string(), "foo.com".to_string());
    assert!(rule.match_url("http://x.com/foo", Some(&params)));

    params.insert("domain".to_string(), "baz.com".to_string());
    assert!(!rule.match_url("http://x.com/foo", Some(&params)));

    params.clear();
    assert!(!rule.match_url("http://x.com/foo", Some(&params)));
}