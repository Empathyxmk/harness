use rveachkc_pymsteams::pymsteams::*;
use serde_json::{json, Value};

#[test]
fn test_connectorcard_init_and_summary_public() {
    let url = "https://somedomain.com/webhook/unique_id";
    let mut c = connectorcard(url);
    assert_eq!(c.hookurl, url);
    c.text("Public Hello Text");
    assert_eq!(c.payload["text"], json!("Public Hello Text"));
    c.summary("Public Summary");
    assert_eq!(c.payload["summary"], json!("Public Summary"));
    c.title("Some Public Title");
    assert_eq!(c.payload["title"], json!("Some Public Title"));
    c.color("ABCDEF");
    assert_eq!(c.payload["themeColor"], json!("ABCDEF"));
    let mut section = cardsection();
    section.activityImage("https://images.example.com/pic.png");
    assert_eq!(section.payload["activityImage"], json!("https://images.example.com/pic.png"));
    section.activityTitle("Demo Action");
    assert_eq!(section.payload["activityTitle"], json!("Demo Action"));
    section.activitySubtitle("demo subtitle");
    assert_eq!(section.payload["activitySubtitle"], json!("demo subtitle"));
    section.activityText("some public activity text");
    assert_eq!(section.payload["activityText"], json!("some public activity text"));
    let payload = &c.payload;
    assert!(payload.is_object());
    let dumped = serde_json::to_string(payload).unwrap();
    assert!(dumped.is_string());
}

#[test]
fn test_connectorcard_addSection_public() {
    let url = "https://somedomain.com/webhook/other_id";
    let mut c = connectorcard(url);
    let mut section = cardsection();
    section.title("Public Section2 Title");
    c.addSection(section);
    assert!(c.payload.get("sections").is_some());
    assert_eq!(c.payload["sections"][0]["title"], json!("Public Section2 Title"));
}

#[test]
fn test_connectorcard_addPotentialAction_public() {
    let url = "https://somedomain.com/webhook/pa_id";
    let mut c = connectorcard(url);
    let pa = potentialaction("otherOpenUri");
    c.addPotentialAction(pa);
    assert!(c.payload.get("potentialAction").is_some());
    assert_eq!(c.payload["potentialAction"][0]["@type"], json!("ActionCard"));
}

#[test]
fn test_connectorcard_send_request_public() {
    let url = "https://somedomain.com/webhook/send_id";
    let mut c = connectorcard(url);
    c.text("another post");
    let result = c.send(201);
    assert!(result.is_ok());
}

#[test]
fn test_connectorcard_send_request_error_public() {
    let url = "https://somedomain.com/webhook/send_error";
    let mut c = connectorcard(url);
    c.text("posting error test");
    let result = c.send(404);
    assert!(result.is_err());
}