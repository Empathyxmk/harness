use rveachkc_pymsteams::pymsteams::*;
use serde_json::{json, Value};

#[test]
fn test_connectorcard_init_and_summary() {
    let url = "https://outlook.office.com/webhook/dummy_url";
    let mut c = connectorcard(url);
    assert_eq!(c.hookurl, url);
    c.text("Hello World");
    assert_eq!(c.payload["text"], json!("Hello World"));
    c.summary("Summary");
    assert_eq!(c.payload["summary"], json!("Summary"));
    c.title("A title here");
    assert_eq!(c.payload["title"], json!("A title here"));
    c.color("123456");
    assert_eq!(c.payload["themeColor"], json!("123456"));
    let mut section = cardsection();
    section.activityImage("https://i/image.png");
    assert_eq!(section.payload["activityImage"], json!("https://i/image.png"));
    section.activityTitle("Do Something");
    assert_eq!(section.payload["activityTitle"], json!("Do Something"));
    section.activitySubtitle("subtitle");
    assert_eq!(section.payload["activitySubtitle"], json!("subtitle"));
    section.activityText("text activity");
    assert_eq!(section.payload["activityText"], json!("text activity"));
    let payload = &c.payload;
    assert!(payload.is_object());
    let dumped = serde_json::to_string(payload).unwrap();
    assert!(dumped.is_string());
}

#[test]
fn test_connectorcard_addSection() {
    let url = "https://outlook.office.com/webhook/dummy_url";
    let mut c = connectorcard(url);
    let mut section = cardsection();
    section.title("Section1 Title");
    c.addSection(section);
    assert!(c.payload.get("sections").is_some());
    assert_eq!(c.payload["sections"][0]["title"], json!("Section1 Title"));
}

#[test]
fn test_connectorcard_addPotentialAction() {
    let url = "https://outlook.office.com/webhook/dummy_url";
    let mut c = connectorcard(url);
    let pa = potentialaction("openUri");
    c.addPotentialAction(pa);
    assert!(c.payload.get("potentialAction").is_some());
    assert_eq!(c.payload["potentialAction"][0]["@type"], json!("ActionCard"));
}

#[test]
fn test_connectorcard_send_request() {
    let url = "https://outlook.office.com/webhook/dummy_url";
    let mut c = connectorcard(url);
    c.text("posting");
    let result = c.send(200);
    assert!(result.is_ok());
}

#[test]
fn test_connectorcard_send_request_error() {
    let url = "https://outlook.office.com/webhook/dummy_url";
    let mut c = connectorcard(url);
    c.text("posting error");
    let result = c.send(400);
    assert!(result.is_err());
}