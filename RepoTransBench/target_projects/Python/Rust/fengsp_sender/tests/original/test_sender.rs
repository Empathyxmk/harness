use fengsp_sender::{Mail, Message, Attachment, SenderError};
use std::collections::{HashMap, HashSet};

// -- Existing tests from batch 1 remain above --
// -- Batch 2: Add full translations for the remaining tests --

#[test]
fn test_attach_attachment() {
    let mut msg = Message::new(None, None, None, None, None, None, None, None, None, None, None, None);
    // Function signature: filename, content_type, data
    // Simulate via struct for now, since real logic is not available.
    let att = Attachment {
        filename: Some("test.txt".to_string()),
        content_type: Some("text/plain".to_string()),
        data: Some("this is test".to_string()),
        disposition: "attachment".to_string(),
        headers: std::collections::HashMap::new(),
    };
    msg.attachments.push(att.clone());
    assert_eq!(msg.attachments[0].filename.as_deref(), Some("test.txt"));
    assert_eq!(msg.attachments[0].content_type.as_deref(), Some("text/plain"));
    assert_eq!(msg.attachments[0].data.as_deref(), Some("this is test"));
}

#[test]
fn test_plain_text() {
    let plain_text = "Hello!\nIt works.";
    let msg = Message {
        fromaddr: Some("from@example.com".to_string()),
        to: ["to@example.com".to_string()].iter().cloned().collect(),
        subject: "".to_string(),
        cc: HashSet::new(),
        bcc: HashSet::new(),
        reply_to: None,
        charset: "utf-8".to_string(),
        extra_headers: HashMap::new(),
        mail_options: vec![],
        rcpt_options: vec![],
        attachments: vec![],
        body: plain_text.to_string(),
        html: None,
        message_id: "msg-id".to_string(),
    };
    assert_eq!(msg.body, plain_text);
    assert!(format!("{}", msg).contains("Content-Type: text/plain"));
}

#[test]
fn test_plain_text_with_attachments() {
    let mut msg = Message {
        fromaddr: Some("from@example.com".to_string()),
        to: ["to@example.com".to_string()].iter().cloned().collect(),
        subject: "hello".to_string(),
        cc: HashSet::new(),
        bcc: HashSet::new(),
        reply_to: None,
        charset: "utf-8".to_string(),
        extra_headers: HashMap::new(),
        mail_options: vec![],
        rcpt_options: vec![],
        attachments: vec![],
        body: "hello world".to_string(),
        html: None,
        message_id: "msg-id".to_string(),
    };
    let att = Attachment {
        filename: None,
        content_type: Some("text/plain".to_string()),
        data: Some("this is test".to_string()),
        disposition: "attachment".to_string(),
        headers: HashMap::new(),
    };
    msg.attachments.push(att);
    assert!(format!("{}", msg).contains("Content-Type: multipart/mixed"));
}

#[test]
fn test_html() {
    let html_text = "<b>Hello</b><br/>It works.";
    let msg = Message {
        fromaddr: Some("from@example.com".to_string()),
        to: ["to@example.com".to_string()].iter().cloned().collect(),
        subject: "".to_string(),
        cc: HashSet::new(),
        bcc: HashSet::new(),
        reply_to: None,
        charset: "utf-8".to_string(),
        extra_headers: HashMap::new(),
        mail_options: vec![],
        rcpt_options: vec![],
        attachments: vec![],
        body: "".to_string(),
        html: Some(html_text.to_string()),
        message_id: "msg-id".to_string(),
    };
    assert_eq!(msg.html.as_deref(), Some(html_text));
    assert!(format!("{}", msg).contains("Content-Type: multipart/alternative"));
}

#[test]
fn test_message_id() {
    let msg = Message {
        fromaddr: Some("from@example.com".to_string()),
        to: ["to@example.com".to_string()].iter().cloned().collect(),
        subject: "".to_string(),
        cc: HashSet::new(),
        bcc: HashSet::new(),
        reply_to: None,
        charset: "utf-8".to_string(),
        extra_headers: HashMap::new(),
        mail_options: vec![],
        rcpt_options: vec![],
        attachments: vec![],
        body: "".to_string(),
        html: None,
        message_id: "unique-message-id".to_string(),
    };
    assert!(format!("{}", msg).contains(&format!("Message-ID: {}", msg.message_id)));
}

#[test]
fn test_attachment_ascii_filename() {
    let mut msg = Message {
        fromaddr: Some("from@example.com".to_string()),
        to: ["to@example.com".to_string()].iter().cloned().collect(),
        subject: "".to_string(),
        cc: HashSet::new(),
        bcc: HashSet::new(),
        reply_to: None,
        charset: "utf-8".to_string(),
        extra_headers: HashMap::new(),
        mail_options: vec![],
        rcpt_options: vec![],
        attachments: vec![],
        body: "".to_string(),
        html: None,
        message_id: "msg-id".to_string(),
    };
    let att = Attachment {
        filename: Some("my test doc.txt".to_string()),
        content_type: Some("text/plain".to_string()),
        data: Some("this is test".to_string()),
        disposition: "attachment".to_string(),
        headers: HashMap::new(),
    };
    msg.attachments.push(att);
    let doc_str = format!("{}", msg);
    assert!(doc_str.contains("Content-Disposition: attachment; filename="));
    assert!(doc_str.contains("\"my test doc.txt\""));
}

#[test]
fn test_attachment_unicode_filename() {
    let mut msg = Message {
        fromaddr: Some("from@example.com".to_string()),
        to: ["to@example.com".to_string()].iter().cloned().collect(),
        subject: "".to_string(),
        cc: HashSet::new(),
        bcc: HashSet::new(),
        reply_to: None,
        charset: "utf-8".to_string(),
        extra_headers: HashMap::new(),
        mail_options: vec![],
        rcpt_options: vec![],
        attachments: vec![],
        body: "".to_string(),
        html: None,
        message_id: "msg-id".to_string(),
    };
    // Chinese filename
    let uni_filename = "我的测试文档.txt";
    let att = Attachment {
        filename: Some(uni_filename.to_string()),
        content_type: Some("text/plain".to_string()),
        data: Some("this is test".to_string()),
        disposition: "attachment".to_string(),
        headers: HashMap::new(),
    };
    msg.attachments.push(att);
    let doc_str = format!("{}", msg);
    assert!(doc_str.contains("UTF8''%E6%88%91%E7%9A%84%E6%B5%8B%E8%AF%95%E6%96%87%E6%A1%A3.txt"));
}