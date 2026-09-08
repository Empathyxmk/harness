use crate::urls::resolve;

#[test]
fn test_urls_resolve_latest_issue() {
    let result = resolve("/newsfeed/").unwrap();
    assert_eq!(result, "newsfeed:latest_issue");
}

#[test]
fn test_urls_resolve_issue_list() {
    let result = resolve("/newsfeed/issues/").unwrap();
    assert_eq!(result, "newsfeed:issue_list");
}

#[test]
fn test_urls_resolve_issue_detail() {
    let result = resolve("/newsfeed/issues/any/").unwrap();
    assert_eq!(result, "newsfeed:issue_detail");
}

#[test]
fn test_urls_resolve_subscribe() {
    let result = resolve("/newsfeed/subscribe/").unwrap();
    assert_eq!(result, "newsfeed:newsletter_subscribe");
}

#[test]
fn test_urls_resolve_subscription_confirm() {
    let token = "b8eb9618-eafe-4a98-9463-8925d423dacf";
    let url = format!("/newsfeed/subscribe/confirm/{}/", token);
    let result = resolve(&url).unwrap();
    assert_eq!(result, "newsfeed:newsletter_subscription_confirm");
}

#[test]
fn test_urls_resolve_unsubscribe() {
    let result = resolve("/newsfeed/unsubscribe/").unwrap();
    assert_eq!(result, "newsfeed:newsletter_unsubscribe");
}