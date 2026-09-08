use requests_oauthlib_rs::compliance_fixes;

#[test]
fn test_facebook_fixes_public() {
    let fixed = compliance_fixes::facebook::facebook_compliance_fix(|x: String| x);
    // Succeeds if returned callable
}

#[test]
fn test_mailchimp_fixes_public() {
    let fixed = compliance_fixes::mailchimp::mailchimp_compliance_fix(|x: String| x);
}

#[test]
fn test_fitbit_fixes_public() {
    let fixed = compliance_fixes::fitbit::fitbit_compliance_fix(|x: String| x);
}

#[test]
fn test_slack_fixes_public() {
    let fixed = compliance_fixes::slack::slack_compliance_fix(|x: String| x);
}