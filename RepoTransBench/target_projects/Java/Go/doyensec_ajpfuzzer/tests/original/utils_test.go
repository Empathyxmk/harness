package original

import (
	"regexp"
	"testing"

	"ajpfuzzer"
)

func TestRandomStringNegativeLength(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for negative length")
		}
	}()
	ajpfuzzer.RandomString(-1, "abc")
}

func TestRandomStringWithEmptyChars(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for empty chars")
		}
	}()
	ajpfuzzer.RandomString(5, "")
}

func TestRandomStringWithValidInput(t *testing.T) {
	res := ajpfuzzer.RandomString(8, "abcd")
	if len(res) != 8 {
		t.Errorf("Expected length 8, got %d", len(res))
	}
	match, _ := regexp.MatchString("^[abcd]{8}$", res)
	if !match {
		t.Errorf("Result %q does not match [abcd]{8}", res)
	}
}

func TestGetRandomIntEdgeCases(t *testing.T) {
	if ajpfuzzer.GetRandomInt(5, 5) != 5 {
		t.Errorf("Expected 5 for (5,5)")
	}
	if ajpfuzzer.GetRandomInt(42, 42) != 42 {
		t.Errorf("Expected 42 for (42,42)")
	}
}

func TestGetRandomIntRange(t *testing.T) {
	for i := 0; i < 100; i++ {
		res := ajpfuzzer.GetRandomInt(10, 20)
		if res < 10 || res > 20 {
			t.Errorf("Random value %d not in range 10..20", res)
		}
	}
}

func TestCreateMapFromPairsEvenArguments(t *testing.T) {
	m := ajpfuzzer.CreateMapFromPairs("k1", 123, "k2", "vv", "k3", nil)
	if m["k1"] != 123 {
		t.Errorf("Key k1 expected 123")
	}
	if m["k2"] != "vv" {
		t.Errorf("Key k2 expected 'vv'")
	}
	if m["k3"] != nil {
		t.Errorf("Key k3 expected nil, got %v", m["k3"])
	}
	if len(m) != 3 {
		t.Errorf("Expected map size 3")
	}
}

func TestCreateMapFromPairsOddArguments(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for odd number of args")
		}
	}()
	ajpfuzzer.CreateMapFromPairs("a", "b", "c")
}

func TestToHex(t *testing.T) {
	b := []byte{0, 10, 15, 16, 31, 127, 255}
	hex := ajpfuzzer.ToHex(b)
	match, _ := regexp.MatchString("^[0-9a-f]{14}$", hex)
	if !match {
		t.Errorf("Hex result %q does not match [0-9a-f]{14}", hex)
	}
	if hex != "000a0f101f7fff" {
		t.Errorf("Expected '000a0f101f7fff', got %s", hex)
	}
}

func TestToHexNull(t *testing.T) {
	if res := ajpfuzzer.ToHex(nil); res != "" {
		t.Errorf("Expected empty string for nil, got %q", res)
	}
}

func TestToHexEmpty(t *testing.T) {
	if res := ajpfuzzer.ToHex([]byte{}); res != "" {
		t.Errorf("Expected empty string for empty byte array, got %q", res)
	}
}

func TestJoinSimple(t *testing.T) {
	arr := []string{"a", "b", "c"}
	result := ajpfuzzer.Join(arr, ":")
	if result != "a:b:c" {
		t.Errorf("Expected 'a:b:c', got %q", result)
	}
}

func TestJoinNull(t *testing.T) {
	if ajpfuzzer.Join(nil, ",") != "" {
		t.Errorf("Expected empty string for nil input")
	}
}

func TestJoinEmptyArray(t *testing.T) {
	if ajpfuzzer.Join([]string{}, "|") != "" {
		t.Errorf("Expected empty string for empty array")
	}
}

func TestJoinNoSeparator(t *testing.T) {
	arr := []string{"x", "y"}
	if ajpfuzzer.Join(arr, "") != "xy" {
		t.Errorf("Expected 'xy', got %q", ajpfuzzer.Join(arr, ""))
	}
}