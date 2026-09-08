package tests

import (
	"encoding/json"
	"reflect"
	"testing"

	"rveachkc_pymsteams/pymsteams"
)

func TestConnectorCardInitAndSummary(t *testing.T) {
	url := "https://outlook.office.com/webhook/dummy_url"
	c := pymsteams.NewConnectorCard(url)
	if c.hookurl != url {
		t.Error("hookurl mismatch")
	}
	c.text("Hello World")
	if c.payload["text"] != "Hello World" {
		t.Error("text not set")
	}
	c.summary("Summary")
	if c.payload["summary"] != "Summary" {
		t.Error("summary not set")
	}
	c.title("A title here")
	if c.payload["title"] != "A title here" {
		t.Error("title not set")
	}
	c.color("123456")
	if c.payload["themeColor"] != "123456" {
		t.Error("themeColor not set")
	}
	section := pymsteams.NewCardSection()
	section.activityImage("https://i/image.png")
	if section.payload["activityImage"] != "https://i/image.png" {
		t.Error("activityImage incorrect")
	}
	section.activityTitle("Do Something")
	if section.payload["activityTitle"] != "Do Something" {
		t.Error("activityTitle incorrect")
	}
	section.activitySubtitle("subtitle")
	if section.payload["activitySubtitle"] != "subtitle" {
		t.Error("activitySubtitle incorrect")
	}
	section.activityText("text activity")
	if section.payload["activityText"] != "text activity" {
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

func TestConnectorCardAddSection(t *testing.T) {
	url := "https://outlook.office.com/webhook/dummy_url"
	c := pymsteams.NewConnectorCard(url)
	section := pymsteams.NewCardSection()
	section.title("Section1 Title")
	c.addSection(section)
	sections, ok := c.payload["sections"].([]interface{})
	if !ok || len(sections) == 0 {
		t.Error("no sections added")
	}
	secm, ok := sections[0].(map[string]interface{})
	if !ok {
		t.Error("section not a map")
	}
	if secm["title"] != "Section1 Title" {
		t.Error("section title mismatch")
	}
}

func TestConnectorCardAddPotentialAction(t *testing.T) {
	url := "https://outlook.office.com/webhook/dummy_url"
	c := pymsteams.NewConnectorCard(url)
	pa := pymsteams.NewPotentialAction("openUri")
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

func TestConnectorCardSendRequest(t *testing.T) {
	url := "https://outlook.office.com/webhook/dummy_url"
	c := pymsteams.NewConnectorCard(url)
	c.text("posting")
	err := c.send(pymsteams.DummyPostSuccess)
	if err != nil {
		t.Errorf("send did not return nil, got: %v", err)
	}
}

func TestConnectorCardSendRequestError(t *testing.T) {
	url := "https://outlook.office.com/webhook/dummy_url"
	c := pymsteams.NewConnectorCard(url)
	c.text("posting error")
	err := c.send(pymsteams.DummyPostErr)
	if err == nil {
		t.Errorf("send did not raise error for bad response")
	}
}