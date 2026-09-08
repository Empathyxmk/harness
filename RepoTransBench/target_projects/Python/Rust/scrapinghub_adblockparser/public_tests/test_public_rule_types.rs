use scrapinghub_adblockparser::adblockparser::AdblockRule;

const COMMENT_RULES: &[&str] = &[
    "! This is a comment line",
    "! Title: Example Filter List",
    "! Expires: 4 days",
    "! Homepage: https://example.com/",
    "[Adblock]",
    "!#include another_list.txt",
];

const HTML_RULES: &[&str] = &[
    "##.bannerAd",
    "@@##.sponsoredContent",
    "mysite.com#@##sidebar",
    "@@##.cookieBar",
    "example.net,example.org#@##promo",
    "##a[href^='https://tracker.example.com/']",
    "##img[src$=\".ads.png\"]",
];

#[test]
fn test_public_is_comment() {
    for &text in COMMENT_RULES {
        let rule = AdblockRule::new(text);
        assert!(rule.is_comment);
        assert!(!rule.is_html_rule);
        assert!(!rule.is_exception);
        assert!(rule.options.is_empty());
        assert!(rule.regex.is_none());
    }
}

#[test]
fn test_public_is_html_rule() {
    for &text in HTML_RULES {
        let rule = AdblockRule::new(text);
        assert!(rule.is_html_rule);
        assert!(!rule.is_comment);
    }
}