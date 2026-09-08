use crate::admin::*;
use crate::models::*;
use chrono::Utc;

#[test]
fn test_publish_issues_action() {
    let mut issue = Issue::new(1, "Test Issue", true, Utc::now(), 1);
    let mut issues = vec![issue.clone()];
    {
        let mut data = super::admin::ISSUES.lock().unwrap();
        *data = issues.clone();
    }
    assert!(issue.is_draft);

    publish_issues_action(&[1]);
    let data = super::admin::ISSUES.lock().unwrap();
    assert!(!data[0].is_draft);
}

#[test]
fn test_make_draft_action() {
    let mut issue = Issue::new(2, "Released", false, Utc::now(), 2);
    let mut issues = vec![issue.clone()];
    {
        let mut data = super::admin::ISSUES.lock().unwrap();
        *data = issues.clone();
    }
    assert!(!issue.is_draft);

    make_draft_action(&[2]);
    let data = super::admin::ISSUES.lock().unwrap();
    assert!(data[0].is_draft);
}

#[test]
fn test_send_newsletters_action() {
    let mut newsletter = Newsletter::new(1, "Newsletter", false, Utc::now(), None);
    let newsletters = vec![newsletter.clone()];
    {
        let mut data = super::admin::NEWSLETTERS.lock().unwrap();
        *data = newsletters.clone();
    }
    let count = send_newsletters_action(&[1]);
    let data = super::admin::NEWSLETTERS.lock().unwrap();
    assert_eq!(count, 1);
    assert!(data[0].is_sent);
}

#[test]
fn test_hide_post_action() {
    let mut post = Post::new(1, "Visible Post", true, None, None);
    {
        let mut data = super::admin::POSTS.lock().unwrap();
        *data = vec![post.clone()];
    }
    assert!(post.is_visible);

    hide_post_action(&[1]);
    let data = super::admin::POSTS.lock().unwrap();
    assert!(!data[0].is_visible);
}

#[test]
fn test_make_post_visible_action() {
    let mut post = Post::new(2, "Invisible Post", false, None, None);
    {
        let mut data = super::admin::POSTS.lock().unwrap();
        *data = vec![post.clone()];
    }
    assert!(!post.is_visible);

    make_post_visible_action(&[2]);
    let data = super::admin::POSTS.lock().unwrap();
    assert!(data[0].is_visible);
}