#[test]
fn test_imports_available() {
    use scrapinghub_adblockparser::adblockparser::{AdblockRule, AdblockRules};
    let _ = AdblockRule::new("test");
    let _ = AdblockRules::new(vec!["test"]);
}