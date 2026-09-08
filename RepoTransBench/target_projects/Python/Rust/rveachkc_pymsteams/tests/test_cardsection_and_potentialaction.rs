use rveachkc_pymsteams::pymsteams::*;
use serde_json::{json, Value};

#[test]
fn test_cardsection_basic() {
    let mut section = cardsection();
    assert!(std::ptr::eq(section.title("title text"), &section));
    assert_eq!(section.payload["title"], json!("title text"));
    assert_eq!(section.activityTitle("activity").payload["activityTitle"], json!("activity"));
    assert_eq!(section.activitySubtitle("subtitle").payload["activitySubtitle"], json!("subtitle"));
    assert_eq!(section.activityImage("http://image.png").payload["activityImage"], json!("http://image.png"));
    assert_eq!(section.activityText("text here").payload["activityText"], json!("text here"));
    assert_eq!(section.text("hello").payload["text"], json!("hello"));
    assert_eq!(section.linkButton("Go", "http://go.com").payload["potentialAction"][0]["name"], json!("Go"));
    assert_eq!(section.disableMarkdown().payload["markdown"], json!(false));
    assert_eq!(section.enableMarkdown().payload["markdown"], json!(true));
    let dumped = section.dumpSection();
    assert!(dumped.is_object());
}

#[test]
fn test_cardsection_addFact_and_addImage() {
    let mut section = cardsection();
    section.addFact("f1", "v1");
    assert_eq!(section.payload["facts"], json!([{"name": "f1", "value": "v1"}]));
    section.addFact("f2", "v2");
    assert_eq!(section.payload["facts"].as_array().unwrap().len(), 2);
    section.addImage("http://img.com/img.jpg", Some("image1"));
    assert_eq!(section.payload["images"][0]["title"], json!("image1"));
    section.addImage("http://img.com/img2.jpg", None);
    assert!(!section.payload["images"][1].get("title").is_some());
}

#[test]
fn test_cardsection_fact_and_image_keys() {
    let mut section = cardsection();
    section.payload["facts"] = json!([{"name": "start", "value": "val"}]);
    section.addFact("foo", "bar");
    assert_eq!(section.payload["facts"].as_array().unwrap().len(), 2);
    section.payload["images"] = json!([{"image": "test"}]);
    section.addImage("img-url", None);
    assert_eq!(section.payload["images"].as_array().unwrap().len(), 2);
}

#[test]
fn test_potentialaction_inputs_and_actions() {
    let mut pa = potentialaction("TestAction");
    pa.addInput("TextInput", "inputid", "My Title", true);
    assert_eq!(pa.payload["inputs"][0]["isMultiline"], json!(true));

    pa.addInput("ChoiceInput", "input2", "Another", false);
    pa.addChoice("display", "value");
    assert!(pa.payload["inputs"].last().unwrap().get("choices").is_some());

    pa.addAction("ActionType", "ActionName", vec!["http://example.com"], None);
    assert_eq!(pa.payload["actions"][0]["@type"], json!("ActionType"));
    pa.addAction("type", "name", vec!["url"], Some("body here"));
    assert_eq!(pa.payload["actions"][1]["body"], json!("body here"));
}

#[test]
fn test_potentialaction_addOpenURI_and_exceptions() {
    let mut pa = potentialaction("opentest");
    let targets = json!([{"os": "default", "uri": "https://foo.bar/"}]);
    let res = pa.addOpenURI("OpenName", &targets);
    assert!(res.is_ok());
    assert_eq!(res.as_ref().unwrap().payload["targets"], targets);

    let fail = pa.addOpenURI("Broken", &json!("notalist"));
    assert!(fail.is_err());
}

#[test]
fn test_potentialaction_dump() {
    let pa = potentialaction("dumpTest");
    let dumped = pa.dumpPotentialAction();
    assert!(dumped.is_object());
}

#[test]
fn test_TeamsWebhookException_repr() {
    let ex = TeamsWebhookException::new("fail");
    let s = format!("{}", ex);
    assert!(s.contains("fail"));
}