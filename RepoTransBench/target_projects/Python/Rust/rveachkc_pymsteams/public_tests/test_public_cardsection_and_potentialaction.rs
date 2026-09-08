use rveachkc_pymsteams::pymsteams::*;
use serde_json::{json, Value};

#[test]
fn test_cardsection_basic_public() {
    let mut section = cardsection();
    assert!(std::ptr::eq(section.title("Public Section Title"), &section));
    assert_eq!(section.payload["title"], json!("Public Section Title"));
    assert_eq!(section.activityTitle("public activity").payload["activityTitle"], json!("public activity"));
    assert_eq!(section.activitySubtitle("public subtitle").payload["activitySubtitle"], json!("public subtitle"));
    assert_eq!(section.activityImage("https://example.com/img.png").payload["activityImage"], json!("https://example.com/img.png"));
    assert_eq!(section.activityText("public text here").payload["activityText"], json!("public text here"));
    assert_eq!(section.text("greetings").payload["text"], json!("greetings"));
    assert_eq!(section.linkButton("Visit", "https://visit.com").payload["potentialAction"][0]["name"], json!("Visit"));
    assert_eq!(section.disableMarkdown().payload["markdown"], json!(false));
    assert_eq!(section.enableMarkdown().payload["markdown"], json!(true));
    let dumped = section.dumpSection();
    assert!(dumped.is_object());
}

#[test]
fn test_cardsection_addFact_and_addImage_public() {
    let mut section = cardsection();
    section.addFact("fact_one", "value_one");
    assert_eq!(section.payload["facts"], json!([{"name": "fact_one", "value": "value_one"}]));
    section.addFact("fact_two", "value_two");
    assert_eq!(section.payload["facts"].as_array().unwrap().len(), 2);
    section.addImage("https://img-server.com/photo1.jpg", Some("photo title"));
    assert_eq!(section.payload["images"][0]["title"], json!("photo title"));
    section.addImage("https://img-server.com/photo2.jpg", None);
    assert!(!section.payload["images"][1].get("title").is_some());
}

#[test]
fn test_cardsection_fact_and_image_keys_public() {
    let mut section = cardsection();
    section.payload["facts"] = json!([{"name": "init_name", "value": "init_val"}]);
    section.addFact("another_name", "another_val");
    assert_eq!(section.payload["facts"].as_array().unwrap().len(), 2);
    section.payload["images"] = json!([{"image": "img_obj"}]);
    section.addImage("more-img-url", None);
    assert_eq!(section.payload["images"].as_array().unwrap().len(), 2);
}

#[test]
fn test_potentialaction_inputs_and_actions_public() {
    let mut pa = potentialaction("PublicAction");
    pa.addInput("TextInput", "pub_input", "Public Input Title", false);
    assert_eq!(pa.payload["inputs"][0]["isMultiline"], json!(false));

    pa.addInput("ChoiceInput", "pub_input2", "Public Choice Input", true);
    pa.addChoice("pub_display", "pub_value");
    assert!(pa.payload["inputs"].last().unwrap().get("choices").is_some());

    pa.addAction("CustomActionType", "ActionPublic", vec!["https://example.org"], None);
    assert_eq!(pa.payload["actions"][0]["@type"], json!("CustomActionType"));
    pa.addAction("secondtype", "publicaction", vec!["weburl"], Some("some body here"));
    assert_eq!(pa.payload["actions"][1]["body"], json!("some body here"));
}

#[test]
fn test_potentialaction_addOpenURI_and_exceptions_public() {
    let mut pa = potentialaction("testopen");
    let targets = json!([{"os": "mobile", "uri": "https://other-url.com/"}]);
    let res = pa.addOpenURI("OpenOther", &targets);
    assert!(res.is_ok());
    assert_eq!(res.as_ref().unwrap().payload["targets"], targets);

    let fail = pa.addOpenURI("Failer", &json!(12345));
    assert!(fail.is_err());
}

#[test]
fn test_potentialaction_dump_public() {
    let pa = potentialaction("dumpPA");
    let dumped = pa.dumpPotentialAction();
    assert!(dumped.is_object());
}

#[test]
fn test_TeamsWebhookException_repr_public() {
    let ex = TeamsWebhookException::new("public fail");
    let s = format!("{}", ex);
    assert!(s.contains("public fail"));
}