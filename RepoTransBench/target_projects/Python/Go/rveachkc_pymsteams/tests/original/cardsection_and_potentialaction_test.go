package tests

import (
	"reflect"
	"testing"

	"rveachkc_pymsteams/pymsteams"
)

func TestCardSectionBasic(t *testing.T) {
	section := pymsteams.NewCardSection()
	if section.title("title text") != section {
		t.Error("title func should return self")
	}
	if section.payload["title"] != "title text" {
		t.Errorf("payload.title mismatch: %v", section.payload["title"])
	}
	if section.activityTitle("activity").payload["activityTitle"] != "activity" {
		t.Error("activityTitle payload mismatch")
	}
	if section.activitySubtitle("subtitle").payload["activitySubtitle"] != "subtitle" {
		t.Error("activitySubtitle payload mismatch")
	}
	if section.activityImage("http://image.png").payload["activityImage"] != "http://image.png" {
		t.Error("activityImage mismatch")
	}
	if section.activityText("text here").payload["activityText"] != "text here" {
		t.Error("activityText mismatch")
	}
	if section.text("hello").payload["text"] != "hello" {
		t.Error("text mismatch")
	}
	section.linkButton("Go", "http://go.com")
	actions, ok := section.payload["potentialAction"].([]interface{})
	if !ok || len(actions) == 0 {
		t.Fatal("missing potentialAction or wrong type")
	}
	first, ok := actions[0].(map[string]interface{})
	if !ok || first["name"] != "Go" {
		t.Error("linkButton not set properly")
	}
	if section.disableMarkdown().payload["markdown"] != false {
		t.Error("disableMarkdown not working")
	}
	if section.enableMarkdown().payload["markdown"] != true {
		t.Error("enableMarkdown not working")
	}
	dumped := section.dumpSection()
	if reflect.TypeOf(dumped).Kind() != reflect.Map {
		t.Error("dumpSection did not return map")
	}
}

func TestCardSectionAddFactAndAddImage(t *testing.T) {
	section := pymsteams.NewCardSection()
	section.addFact("f1", "v1")
	wantFacts := []interface{}{map[string]interface{}{"name": "f1", "value": "v1"}}
	if !reflect.DeepEqual(section.payload["facts"], wantFacts) {
		t.Error("addFact mismatch")
	}
	section.addFact("f2", "v2")
	facts, _ := section.payload["facts"].([]interface{})
	if len(facts) != 2 {
		t.Error("addFact length error")
	}
	section.addImage("http://img.com/img.jpg", "image1")
	images, _ := section.payload["images"].([]interface{})
	img, _ := images[0].(map[string]interface{})
	if img["title"] != "image1" {
		t.Error("addImage title missing")
	}
	section.addImage("http://img.com/img2.jpg")
	images, _ = section.payload["images"].([]interface{})
	_, ok := images[1].(map[string]interface{})
	if !ok {
		t.Fatal("second image not map")
	}
	if _, ok := images[1].(map[string]interface{})["title"]; ok {
		t.Error("title should not exist on second image")
	}
}

func TestCardSectionFactAndImageKeys(t *testing.T) {
	section := pymsteams.NewCardSection()
	section.payload["facts"] = []interface{}{map[string]interface{}{"name": "start", "value": "val"}}
	section.addFact("foo", "bar")
	facts, _ := section.payload["facts"].([]interface{})
	if len(facts) != 2 {
		t.Error("facts len mismatch after addFact")
	}
	section.payload["images"] = []interface{}{map[string]interface{}{"image": "test"}}
	section.addImage("img-url")
	images, _ := section.payload["images"].([]interface{})
	if len(images) != 2 {
		t.Error("images len mismatch after addImage")
	}
}

func TestPotentialActionInputsAndActions(t *testing.T) {
	pa := pymsteams.NewPotentialAction("TestAction")
	pa.addInput("TextInput", "inputid", "My Title", true)
	inputs, _ := pa.payload["inputs"].([]interface{})
	firstmap := inputs[0].(map[string]interface{})
	if b, ok := firstmap["isMultiline"]; !ok || b != true {
		t.Error("TextInput isMultiline not set true")
	}
	pa.addInput("ChoiceInput", "input2", "Another", false)
	pa.addChoice("display", "value")
	inputs, _ = pa.payload["inputs"].([]interface{})
	secondmap := inputs[1].(map[string]interface{})
	if _, ok := secondmap["choices"]; !ok {
		t.Error("ChoiceInput did not set choices")
	}
	pa.addAction("ActionType", "ActionName", []string{"http://example.com"})
	acts, _ := pa.payload["actions"].([]interface{})
	actmap := acts[0].(map[string]interface{})
	if actmap["@type"] != "ActionType" {
		t.Error("addAction type mismatch")
	}
	pa.addAction("type", "name", []string{"url"}, "body here")
	acts, _ = pa.payload["actions"].([]interface{})
	actmap2 := acts[1].(map[string]interface{})
	if actmap2["body"] != "body here" {
		t.Error("addAction body param not set")
	}
}

func TestPotentialActionAddOpenURIAndExceptions(t *testing.T) {
	pa := pymsteams.NewPotentialAction("opentest")
	targets := []map[string]interface{}{{"os": "default", "uri": "https://foo.bar/"}}
	res, err := pa.addOpenURI("OpenName", targets)
	if err != nil {
		t.Errorf("addOpenURI error: %v", err)
	}
	val, ok := res.payload["targets"].([]interface{})
	if !ok || len(val) == 0 {
		t.Error("addOpenURI targets missing")
	}
	_, err = pa.addOpenURI("Broken", "notalist")
	if err == nil {
		t.Error("addOpenURI should error if not list")
	}
}

func TestPotentialActionDump(t *testing.T) {
	pa := pymsteams.NewPotentialAction("dumpTest")
	dumped := pa.dumpPotentialAction()
	if reflect.TypeOf(dumped).Kind() != reflect.Map {
		t.Error("dumpPotentialAction not map")
	}
}

func TestTeamsWebhookExceptionRepr(t *testing.T) {
	ex := pymsteams.NewTeamsWebhookException("fail")
	if ex.Error() != "fail" {
		t.Error("TeamsWebhookException error message")
	}
}