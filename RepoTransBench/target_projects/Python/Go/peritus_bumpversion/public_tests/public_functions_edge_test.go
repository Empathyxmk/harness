package public_tests

import (
	"testing"
	"bumpversion/functions"
)

func TestReplaceNumericPostfixOnlyNumber(t *testing.T) {
	if out := functions.ReplaceNumericPostfix("667", 334); out != "334" {
		t.Errorf("Expected '334', got '%v'", out)
	}
}

func TestFirstNumericMatchIndexNoneNumber(t *testing.T) {
	_, _, ok := functions.FirstNumericMatchIndex("qwerty")
	if ok {
		t.Errorf("Expected no numeric match")
	}
}

func TestFirstAlphaPostfixEdge(t *testing.T) {
	if got := functions.FirstAlphaPostfix("123456"); got != "" {
		t.Errorf("Expected empty string, got '%v'", got)
	}
}

func TestFindFirstNumberComplexString(t *testing.T) {
	val := "xy_hello2abc5"
	if functions.FindFirstNumber(val) != "2" {
		t.Errorf("Expected '2', got '%v'", functions.FindFirstNumber(val))
	}
}

func TestIncrementStringNumberOnlyNumber(t *testing.T) {
	if got := functions.IncrementStringNumber("105"); got != "106" {
		t.Errorf("Expected '106', got '%v'", got)
	}
}

func TestIncrementStringNumberWithZeros(t *testing.T) {
	if got := functions.IncrementStringNumber("code007bond"); got != "code008bond" {
		t.Errorf("Expected 'code008bond', got '%v'", got)
	}
}