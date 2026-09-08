package public_tests

import (
	"testing"

	"github.com/mycompany/app/app"
)

func TestGetMessage_Public(t *testing.T) {
	expected := "Hello Remote World!"
	got := app.GetMessage()
	if got != expected {
		t.Errorf("GetMessage() = %q; want %q", got, expected)
	}
}

func TestEvaluateNumber_PositiveEven_Public(t *testing.T) {
	expected := "Positive Even"
	got := app.EvaluateNumber(8)
	if got != expected {
		t.Errorf("EvaluateNumber(8) = %q; want %q", got, expected)
	}
}

func TestEvaluateNumber_PositiveOdd_Public(t *testing.T) {
	expected := "Positive Odd"
	got := app.EvaluateNumber(15)
	if got != expected {
		t.Errorf("EvaluateNumber(15) = %q; want %q", got, expected)
	}
}

func TestEvaluateNumber_Negative_Public(t *testing.T) {
	expected := "Negative"
	got := app.EvaluateNumber(-123)
	if got != expected {
		t.Errorf("EvaluateNumber(-123) = %q; want %q", got, expected)
	}
}

func TestEvaluateNumber_Zero_Public(t *testing.T) {
	expected := "Zero"
	got := app.EvaluateNumber(0)
	if got != expected {
		t.Errorf("EvaluateNumber(0) = %q; want %q", got, expected)
	}
}