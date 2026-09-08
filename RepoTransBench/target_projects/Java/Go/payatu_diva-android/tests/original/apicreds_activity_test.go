package original

import (
	"testing"
)

// Simulated "TextView" for demonstration.
type TextView struct {
	Text string
}

// Simulated APICredsActivity for testing.
type APICredsActivity struct {
	apicTextView *TextView
}

func NewAPICredsActivity() *APICredsActivity {
	return &APICredsActivity{
		apicTextView: &TextView{
			Text: "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword",
		},
	}
}

func (a *APICredsActivity) FindViewById(id int) *TextView {
	// Only one TextView for test
	return a.apicTextView
}

func TestAPICredsActivity_onCreate_setsAPIText(t *testing.T) {
	activity := NewAPICredsActivity()
	tv := activity.FindViewById(1)
	if tv == nil {
		t.Fatal("Expected non-nil TextView")
	}
	expected := "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword"
	if tv.Text != expected {
		t.Errorf("Expected TextView text: %q, got %q", expected, tv.Text)
	}
}