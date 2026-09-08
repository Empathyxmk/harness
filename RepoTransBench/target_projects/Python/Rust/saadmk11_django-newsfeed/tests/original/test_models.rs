use crate::models::*;
use chrono::{Duration, Utc};

#[test]
fn test_post_str_and_visibility() {
    let post = Post::new(1, "Test Post", true, None, None);
    assert_eq!(post.str_(), "Test Post");
    let invisible_post = Post::new(2, "Invisible", false, None, None);
    assert!(!invisible_post.is_visible);
    assert!(post.is_visible);
}

#[test]
fn test_issue_str_and_published() {
    let issue = Issue::new(1, "Issue", false, Utc::now() - Duration::days(1), 1);
    assert_eq!(issue.str_(), "Issue");
    let unreleased = Issue::new(2, "Draft", true, Utc::now(), 2);
    assert!(!unreleased.is_published());
    assert!(issue.is_published());
}

#[test]
fn test_issue_absolute_url() {
    let issue = Issue::new(8, "Any", false, Utc::now(), 17);
    assert_eq!(issue.get_absolute_url(), "/newsfeed/issues/17/");
}

#[test]
fn test_subscriber_str_and_token_expiry() {
    let mut s = Subscriber::new(1, "abc@xyz.com", false, false, Some(Utc::now() - Duration::days(3)));
    assert_eq!(s.str_(), "abc@xyz.com");
    assert!(s.token_expired());
    s.verification_sent_date = Some(Utc::now());
    assert!(!s.token_expired());
    s.verification_sent_date = None;
    assert!(s.token_expired());
}

#[test]
fn test_subscriber_reset_token() {
    let mut s = Subscriber::new(2, "abc@xyz.com", false, false, None);
    let old_token = s.token.clone();
    s.reset_token();
    assert_ne!(old_token, s.token);
}

#[test]
fn test_subscriber_subscribe_and_unsubscribe() {
    let mut s = Subscriber::new(4, "abc@xyz.com", false, false, Some(Utc::now() - Duration::days(1)));
    // can subscribe
    assert!(!s.verified && !s.subscribed);
    let b = s.subscribe();
    assert!(b);
    assert!(s.verified && s.subscribed);

    let mut s2 = Subscriber::new(5, "z@t.com", false, false, Some(Utc::now() - Duration::days(5)));
    assert!(!s2.subscribe());
    assert!(!s2.verified && !s2.subscribed);

    let mut s3 = Subscriber::new(6, "no@abc.com", false, false, None);
    assert!(!s3.unsubscribe());

    let mut s4 = Subscriber::new(7, "done@def.com", true, true, None);
    let b = s4.unsubscribe();
    assert!(b);
    assert!(!s4.verified && !s4.subscribed);
}

#[test]
fn test_subscriber_verification_url() {
    let s = Subscriber::new(8, "v@t.com", false, false, None);
    assert!(s.get_verification_url().contains(&s.token));
}

#[test]
fn test_newsletter_str() {
    let n = Newsletter::new(77, "Subject", false, Utc::now(), None);
    assert_eq!(n.str_(), "Subject");
}

#[test]
fn test_postcategory_str() {
    let c = PostCategory::new(5, "Cool");
    assert_eq!(c.str_(), "Cool");
}