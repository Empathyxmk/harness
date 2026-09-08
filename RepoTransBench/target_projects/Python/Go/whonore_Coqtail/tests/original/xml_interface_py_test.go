package original

import (
	"encoding/xml"
	"testing"
)

type CoqtailPythonXml struct {
	XMLName xml.Name `xml:"coqtail"`
	Cmd     string   `xml:"cmd,attr"`
	Content string   `xml:",chardata"`
}

func parseCoqtailPythonXml(input string) (string, string, error) {
	var val CoqtailPythonXml
	err := xml.Unmarshal([]byte(input), &val)
	return val.Cmd, val.Content, err
}

func TestParseCoqtailPythonXml(t *testing.T) {
	raw := `<coqtail cmd="expr">42</coqtail>`
	cmd, val, err := parseCoqtailPythonXml(raw)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if cmd != "expr" || val != "42" {
		t.Errorf("Expected expr/42, got %q/%q", cmd, val)
	}
}

func TestParseCoqtailPythonXmlEmpty(t *testing.T) {
	raw := `<coqtail></coqtail>`
	cmd, val, err := parseCoqtailPythonXml(raw)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if cmd != "" || val != "" {
		t.Errorf("Empty test expected, got %q/%q", cmd, val)
	}
}

func TestParseCoqtailPythonXmlMalformed(t *testing.T) {
	raw := `<coqtail cmd="foo">`
	_, _, err := parseCoqtailPythonXml(raw)
	if err == nil {
		t.Errorf("Expected XML error for malformed string")
	}
}