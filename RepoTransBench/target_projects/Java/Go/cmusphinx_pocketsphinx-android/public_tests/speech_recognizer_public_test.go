package public_tests

import "testing"

type SpeechRecognizer struct {}

func NewSpeechRecognizer() *SpeechRecognizer { return &SpeechRecognizer{} }

func TestSpeechRecognizerInstancePublic(t *testing.T) {
	r := NewSpeechRecognizer()
	if r == nil {
		t.Fatal("Expected non-nil SpeechRecognizer instance")
	}
}