package public_tests

import (
	"encoding/json"
	"reflect"
	"testing"

	"rveachkc_pymsteams/pymsteams"
)

func TestConnectorCardInitAndSummaryPublic(t *testing.T) {
	url := "https://somedomain.com/webhook/unique_id"
	c := pymsteams.NewConnectorCard(url)
	if c.hookurl != url {
		t.Error("hookurl mismatch")
	}
	c.text("Public Hello Text")
	if c.payload["text"] != "Public Hello Text" {
		t.Error("text not set")
	}
	c.summary("Public Summary")
	if c.payload["summary"] != "Public Summary" {
		t.Error("summary not set")
	}
	c.title("Some Public Title")
	if c.payload["title"] != "Some Public Title" {
		t.Error("title not set")
	}
	c.color("ABCDEF")
	if c.payload["themeColor"] != "ABCDEF" {
		t.Error("themeColor not set")
	}
	section := pymsteams.NewCardSection()
	section.activityImage("https://images.example.com/pic.png")
	if section.payload["activityImage"] != "https://images.example.com/pic.png" {
		t.Error("activityImage incorrect")
	}
	section.activityTitle("Demo Action")
	if section.payload["activityTitle"] != "Demo Action" {
		t.Error("activityTitle incorrect")
	}
	section.activitySubtitle("demo subtitle")
	if section.payload["activitySubtitle"] != "demo subtitle" {
		t.Error("activitySubtitle incorrect")
	}
	section.activityText("some public activity text")
	if section.payload["activityText"] != "some public activity text" {
		t.Error("activityText incorrect")
	}
	payload := c.payload
	if reflect.TypeOf(payload).Kind() != reflect.Map {
		t.Error("payload is not map")
	}
	dumped, err := json.Marshal(payload)
	if err != nil || reflect.TypeOf(string(dumped)).Kind() != reflect.String {
		t.Error("marshal did not return string")
	}
}

func TestConnectorCardAddSectionPublic(t *testing.T) {
	url := "https://somedomain.com/webhook/other_id"
	c := pymsteams.NewConnectorCard(url)
	section := pymsteams.NewCardSection()
	section.title("Public Section2 Title")
	c.addSection(section)
	sections, ok := c.payload["sections"].([]interface{})
	if !ok || len(sections) == 0 {
		t.Error("no sections added")
	}
	secm, ok := sections[0].(map[string]interface{})
	if !ok {
		t.Error("section not a map")
	}
	if secm["title"] != "Public Section2 Title" {
		t.Error("section title mismatch")
	}
}

func TestConnectorCardAddPotentialActionPublic(t *testing.T) {
	url := "https://somedomain.com/webhook/pa_id"
	c := pymsteams.NewConnectorCard(url)
	pa := pymsteams.NewPotentialAction("otherOpenUri")
	c.addPotentialAction(pa)
	pas, ok := c.payload["potentialAction"].([]interface{})
	if !ok || len(pas) == 0 {
		t.Error("potentialAction not found")
	}
	pam, ok := pas[0].(map[string]interface{})
	if !ok {
		t.Error("potentialAction is not map")
	}
	if pam["@type"] != "ActionCard" {
		t.Error("potentialAction @type not ActionCard")
	}
}

func TestConnectorCardSendRequestPublic(t *testing.T) {
	url := "https://somedomain.com/webhook/send_id"
	c := pymsteams.NewConnectorCard(url)
	c.text("another post")
	err := c.send(pymsteams.DummyPostCreated)
	if err != nil {
		t.Errorf("send did not return nil, got: %v", err)
	}
}

func TestConnectorCardSendRequestErrorPublic(t *testing.T) {
	url := "https://somedomain.com/webhook/send_error"
	c := pymsteams.NewConnectorCard(url)
	c.text("posting error test")
	err := c.send(pymsteams.DummyPostNotFound)
	if err == nil {
		t.Errorf("send did not raise error for bad response")
	}
}