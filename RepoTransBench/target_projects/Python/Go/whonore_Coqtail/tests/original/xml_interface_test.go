package original

import (
	"encoding/xml"
	"reflect"
	"strings"
	"testing"
)

type CoqtailXmlCmd struct {
	XMLName xml.Name `xml:"coqtail"`
	Cmd     string   `xml:"cmd,attr"`
	Text    string   `xml:",chardata"`
}

func parseCoqtailXmlRaw(input string) (CoqtailXmlCmd, error) {
	var cmd CoqtailXmlCmd
	err := xml.Unmarshal([]byte(input), &cmd)
	return cmd, err
}

func TestParseCoqtailXmlRawBasic(t *testing.T) {
	raw := `<coqtail cmd="Hello">world</coqtail>`
	cmd, err := parseCoqtailXmlRaw(raw)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if cmd.Cmd != "Hello" || strings.TrimSpace(cmd.Text) != "world" {
		t.Errorf("ParseCoqtailXmlRaw failed: got %q %q", cmd.Cmd, cmd.Text)
	}
}

func TestParseCoqtailXmlRawMissingCommand(t *testing.T) {
	raw := `<coqtail>text</coqtail>`
	cmd, err := parseCoqtailXmlRaw(raw)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if cmd.Cmd != "" || strings.TrimSpace(cmd.Text) != "text" {
		t.Errorf("Parse error on missing cmd attribute")
	}
}

func TestParseCoqtailXmlRawMalformed(t *testing.T) {
	raw := `<coqtail cmd="Oops">`
	_, err := parseCoqtailXmlRaw(raw)
	if err == nil {
		t.Errorf("Expected XML error from malformed input")
	}
}

func TestParseCoqtailXmlRawAttributes(t *testing.T) {
	raw := `<coqtail cmd="A" x="B">C</coqtail>`
	cmd, err := parseCoqtailXmlRaw(raw)
	if err != nil {
		t.Fatalf("Unexpected error parsing attributes: %v", err)
	}
	if cmd.Cmd != "A" {
		t.Errorf("Expected cmd attribute 'A', got %q", cmd.Cmd)
	}
	if strings.TrimSpace(cmd.Text) != "C" {
		t.Errorf("Expected text 'C', got %q", cmd.Text)
	}
}