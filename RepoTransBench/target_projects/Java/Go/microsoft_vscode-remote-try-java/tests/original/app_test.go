package tests

import (
	"testing"

	"github.com/mycompany/app/app"
)

func TestGetMessage(t *testing.T) {
	expected := "Hello Remote World!"
	got := app.GetMessage()
	if got != expected {
		t.Errorf("GetMessage() = %q; want %q", got, expected)
	}
}

func TestEvaluateNumber_PositiveEven(t *testing.T) {
	expected := "Positive Even"
	got := app.EvaluateNumber(2)
	if got != expected {
		t.Errorf("EvaluateNumber(2) = %q; want %q", got, expected)
	}
}

func TestEvaluateNumber_PositiveOdd(t *testing.T) {
	expected := "Positive Odd"
	got := app.EvaluateNumber(3)
	if got != expected {
		t.Errorf("EvaluateNumber(3) = %q; want %q", got, expected)
	}
}

func TestEvaluateNumber_Negative(t *testing.T) {
	expected := "Negative"
	got := app.EvaluateNumber(-7)
	if got != expected {
		t.Errorf("EvaluateNumber(-7) = %q; want %q", got, expected)
	}
}

func TestEvaluateNumber_Zero(t *testing.T) {
	expected := "Zero"
	got := app.EvaluateNumber(0)
	if got != expected {
		t.Errorf("EvaluateNumber(0) = %q; want %q", got, expected)
	}
}