package public_tests

import (
	"ajpfuzzer"
	"regexp"
	"testing"
)

func TestRandomStringNegativeLengthDifferent(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for negative length")
		}
	}()
	ajpfuzzer.RandomString(-5, "xyz")
}

func TestRandomStringWithEmptyCharsDifferent(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for empty chars")
		}
	}()
	ajpfuzzer.RandomString(3, "")
}

func TestRandomStringWithValidDifferentInput(t *testing.T) {
	result := ajpfuzzer.RandomString(6, "wxyz")
	if len(result) != 6 {
		t.Errorf("Expected length 6, got %d", len(result))
	}
	matched, _ := regexp.MatchString("^[wxyz]{6}$", result)
	if !matched {
		t.Errorf("Result %q does not match [wxyz]{6}", result)
	}
}

func TestGetRandomIntEdgeCasesDifferent(t *testing.T) {
	if ajpfuzzer.GetRandomInt(7, 7) != 7 {
		t.Error("Expected 7 for (7,7)")
	}
	if ajpfuzzer.GetRandomInt(100, 100) != 100 {
		t.Error("Expected 100 for (100,100)")
	}
}

func TestGetRandomIntRangeDifferent(t *testing.T) {
	for i := 0; i < 50; i++ {
		result := ajpfuzzer.GetRandomInt(20, 30)
		if result < 20 || result > 30 {
			t.Errorf("Result %d not in expected range 20..30", result)
		}
	}
}

func TestCreateMapFromPairsEvenArgumentsDifferent(t *testing.T) {
	m := ajpfuzzer.CreateMapFromPairs("key1", 555, "key2", 789, "key3", "value3")
	if len(m) != 3 {
		t.Errorf("Expected size 3, got %d", len(m))
	}
	if m["key1"] != 555 {
		t.Errorf("key1 expected 555")
	}
	if m["key2"] != 789 {
		t.Errorf("key2 expected 789")
	}
	if m["key3"] != "value3" {
		t.Errorf("key3 expected 'value3'")
	}
}

func TestCreateMapFromPairsOddArgumentsDifferent(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for odd number of args")
		}
	}()
	ajpfuzzer.CreateMapFromPairs("foo", "bar", "baz")
}

func TestToHexDifferent(t *testing.T) {
	b := []byte{1, 11, 17, 22, 51, 128, 200}
	hex := ajpfuzzer.ToHex(b)
	matched, _ := regexp.MatchString("^[0-9a-f]{14}$", hex)
	if !matched {
		t.Errorf("Hex result %q does not match [0-9a-f]{14}", hex)
	}
	if hex != "010b11163380c8" {
		t.Errorf("Expected '010b11163380c8', got %s", hex)
	}
}

func TestToHexNullDifferent(t *testing.T) {
	if ajpfuzzer.ToHex(nil) != "" {
		t.Errorf("Expected empty string for nil input")
	}
}

func TestToHexEmptyDifferent(t *testing.T) {
	if ajpfuzzer.ToHex([]byte{}) != "" {
		t.Errorf("Expected empty string for empty slice")
	}
}

func TestJoinSimpleDifferent(t *testing.T) {
	arr := []string{"foo", "bar", "baz"}
	result := ajpfuzzer.Join(arr, "-")
	if result != "foo-bar-baz" {
		t.Errorf("Expected 'foo-bar-baz', got '%s'", result)
	}
}

func TestJoinNullDifferent(t *testing.T) {
	if ajpfuzzer.Join(nil, "&") != "" {
		t.Errorf("Expected empty string for nil input")
	}
}

func TestJoinEmptyArrayDifferent(t *testing.T) {
	if ajpfuzzer.Join([]string{}, "~") != "" {
		t.Errorf("Expected empty string for empty array")
	}
}

func TestJoinNoSeparatorDifferent(t *testing.T) {
	arr := []string{"d", "e", "f"}
	if ajpfuzzer.Join(arr, "") != "def" {
		t.Errorf("Expected 'def', got '%s'", ajpfuzzer.Join(arr, ""))
	}
}