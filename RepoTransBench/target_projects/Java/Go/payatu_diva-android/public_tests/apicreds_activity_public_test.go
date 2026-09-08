package public_tests

import (
	"strings"
	"testing"
)

type TextView struct {
	Text string
}

type APICredsActivity struct {
	apicTextView *TextView
}

func NewAPICredsActivityWithPublicAPIData() *APICredsActivity {
	return &APICredsActivity{
		apicTextView: &TextView{
			Text: "API Key: PUBKEY-8472\nAPI User name: testuser\nAPI Password: pubpass",
		},
	}
}

func (a *APICredsActivity) FindViewById(id int) *TextView {
	return a.apicTextView
}

func TestAPICredsActivity_onCreate_setsAPIText_public(t *testing.T) {
	activity := NewAPICredsActivityWithPublicAPIData()
	tv := activity.FindViewById(1)
	if tv == nil {
		t.Fatal("Expected non-nil TextView")
	}
	notExpected := "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword"
	actual := tv.Text
	if actual == notExpected {
		t.Errorf("Public API text unexpectedly matches the original: %q", actual)
	}
	if !strings.Contains(actual, "API Key:") ||
		!strings.Contains(actual, "API User name:") ||
		!strings.Contains(actual, "API Password:") {
		t.Error("Missing one of required API info in TextView text")
	}
	if strings.Contains(actual, "123secretapikey123") {
		t.Error("TextView text should not contain the original API key")
	}
}