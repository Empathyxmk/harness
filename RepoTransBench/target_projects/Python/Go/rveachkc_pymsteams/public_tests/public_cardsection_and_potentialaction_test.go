package public_tests

import (
	"reflect"
	"testing"

	"rveachkc_pymsteams/pymsteams"
)

func TestCardSectionBasicPublic(t *testing.T) {
	section := pymsteams.NewCardSection()
	if section.title("Public Section Title") != section {
		t.Error("title func should return self")
	}
	if section.payload["title"] != "Public Section Title" {
		t.Errorf("payload.title mismatch: %v", section.payload["title"])
	}
	if section.activityTitle("public activity").payload["activityTitle"] != "public activity" {
		t.Error("activityTitle payload mismatch")
	}
	if section.activitySubtitle("public subtitle").payload["activitySubtitle"] != "public subtitle" {
		t.Error("activitySubtitle payload mismatch")
	}
	if section.activityImage("https://example.com/img.png").payload["activityImage"] != "https://example.com/img.png" {
		t.Error("activityImage mismatch")
	}
	if section.activityText("public text here").payload["activityText"] != "public text here" {
		t.Error("activityText mismatch")
	}
	if section.text("greetings").payload["text"] != "greetings" {
		t.Error("text mismatch")
	}
	section.linkButton("Visit", "https://visit.com")
	actions, ok := section.payload["potentialAction"].([]interface{})
	if !ok || len(actions) == 0 {
		t.Fatal("missing potentialAction or wrong type")
	}
	first, ok := actions[0].(map[string]interface{})
	if !ok || first["name"] != "Visit" {
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

func TestCardSectionAddFactAndAddImagePublic(t *testing.T) {
	section := pymsteams.NewCardSection()
	section.addFact("fact_one", "value_one")
	wantFacts := []interface{}{map[string]interface{}{"name": "fact_one", "value": "value_one"}}
	if !reflect.DeepEqual(section.payload["facts"], wantFacts) {
		t.Error("addFact mismatch")
	}
	section.addFact("fact_two", "value_two")
	facts, _ := section.payload["facts"].([]interface{})
	if len(facts) != 2 {
		t.Error("addFact length error")
	}
	section.addImage("https://img-server.com/photo1.jpg", "photo title")
	images, _ := section.payload["images"].([]interface{})
	img, _ := images[0].(map[string]interface{})
	if img["title"] != "photo title" {
		t.Error("addImage title missing")
	}
	section.addImage("https://img-server.com/photo2.jpg")
	images, _ = section.payload["images"].([]interface{})
	_, ok := images[1].(map[string]interface{})
	if !ok {
		t.Fatal("second image not map")
	}
	if _, ok := images[1].(map[string]interface{})["title"]; ok {
		t.Error("title should not exist on second image")
	}
}

func TestCardSectionFactAndImageKeysPublic(t *testing.T) {
	section := pymsteams.NewCardSection()
	section.payload["facts"] = []interface{}{map[string]interface{}{"name": "init_name", "value": "init_val"}}
	section.addFact("another_name", "another_val")
	facts, _ := section.payload["facts"].([]interface{})
	if len(facts) != 2 {
		t.Error("facts len mismatch after addFact")
	}
	section.payload["images"] = []interface{}{map[string]interface{}{"image": "img_obj"}}
	section.addImage("more-img-url")
	images, _ := section.payload["images"].([]interface{})
	if len(images) != 2 {
		t.Error("images len mismatch after addImage")
	}
}

func TestPotentialActionInputsAndActionsPublic(t *testing.T) {
	pa := pymsteams.NewPotentialAction("PublicAction")
	pa.addInput("TextInput", "pub_input", "Public Input Title", false)
	inputs, _ := pa.payload["inputs"].([]interface{})
	firstmap := inputs[0].(map[string]interface{})
	if b, ok := firstmap["isMultiline"]; !ok || b != false {
		t.Error("TextInput isMultiline not set false")
	}
	pa.addInput("ChoiceInput", "pub_input2", "Public Choice Input", true)
	pa.addChoice("pub_display", "pub_value")
	inputs, _ = pa.payload["inputs"].([]interface{})
	secondmap := inputs[1].(map[string]interface{})
	if _, ok := secondmap["choices"]; !ok {
		t.Error("ChoiceInput did not set choices")
	}
	pa.addAction("CustomActionType", "ActionPublic", []string{"https://example.org"})
	acts, _ := pa.payload["actions"].([]interface{})
	actmap := acts[0].(map[string]interface{})
	if actmap["@type"] != "CustomActionType" {
		t.Error("addAction type mismatch")
	}
	pa.addAction("secondtype", "publicaction", []string{"weburl"}, "some body here")
	acts, _ = pa.payload["actions"].([]interface{})
	actmap2 := acts[1].(map[string]interface{})
	if actmap2["body"] != "some body here" {
		t.Error("addAction body param not set")
	}
}

func TestPotentialActionAddOpenURIAndExceptionsPublic(t *testing.T) {
	pa := pymsteams.NewPotentialAction("testopen")
	targets := []map[string]interface{}{{"os": "mobile", "uri": "https://other-url.com/"}}
	res, err := pa.addOpenURI("OpenOther", targets)
	if err != nil {
		t.Errorf("addOpenURI error: %v", err)
	}
	val, ok := res.payload["targets"].([]interface{})
	if !ok || len(val) == 0 {
		t.Error("addOpenURI targets missing")
	}
	_, err = pa.addOpenURI("Failer", 12345)
	if err == nil {
		t.Error("addOpenURI should error if not list")
	}
}

func TestPotentialActionDumpPublic(t *testing.T) {
	pa := pymsteams.NewPotentialAction("dumpPA")
	dumped := pa.dumpPotentialAction()
	if reflect.TypeOf(dumped).Kind() != reflect.Map {
		t.Error("dumpPotentialAction not map")
	}
}

func TestTeamsWebhookExceptionReprPublic(t *testing.T) {
	ex := pymsteams.NewTeamsWebhookException("public fail")
	if ex.Error() != "public fail" {
		t.Error("TeamsWebhookException error message")
	}
}