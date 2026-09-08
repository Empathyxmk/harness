use scrapinghub_adblockparser::adblockparser::AdblockRule;

const COMMENT_RULES: &[&str] = &[
    "[Adblock Plus 2.0]",
    "! Checksum: nVIXktYXKU6M+cu+Txkhuw",
    "!/cb.php?sub$script,third-party",
    "!@@/cb.php?sub",
    "!###ADSLOT_SKYSCRAPER",
    "! *** easylist:easylist/easylist_whitelist_general_hide.txt ***",
];

const HTML_RULES: &[&str] = &[
    "###ADSLOT_SKYSCRAPER",
    "@@###ADSLOT_SKYSCRAPER",
    "##.adsBox",
    "eee.se#@##adspace_top",
    "domain1.com,domain2.com#@##adwrapper",
    "edgesuitedomain.net#@##ad-unit",
    "mydomain.com#@#.ad-unit",
    "##a[href^=\"http://affiliate.sometracker.com/\"]",
];

#[test]
fn test_is_comment() {
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
fn test_is_html_rule() {
    for &text in HTML_RULES {
        let rule = AdblockRule::new(text);
        assert!(rule.is_html_rule);
        assert!(!rule.is_comment);
    }
}