package public_tests

import (
	"ajpfuzzer"
	"testing"
)

func TestRandomStringAllCharsEdgeDifferent(t *testing.T) {
	result := ajpfuzzer.RandomString(3, "z")
	if result != "zzz" {
		t.Errorf("Expected 'zzz', got '%s'", result)
	}
}

func TestGetRandomIntMinGreaterThanMaxThrowsDifferent(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for min > max")
		}
	}()
	ajpfuzzer.GetRandomInt(10, 2)
}

func TestCreateMapFromPairsTypeSafetyDifferent(t *testing.T) {
	m := ajpfuzzer.CreateMapFromPairs("x", 0.1, "y", 2.2)
	if m["x"] != 0.1 {
		t.Errorf("x expected 0.1, got %v", m["x"])
	}
	if m["y"] != 2.2 {
		t.Errorf("y expected 2.2, got %v", m["y"])
	}
}

func TestToHexUpperByteValuesDifferent(t *testing.T) {
	arr := []byte{0xde, 0xad, 0xbe, 0xef}
	hex := ajpfuzzer.ToHex(arr)
	if hex != "deadbeef" {
		t.Errorf("Expected 'deadbeef', got %s", hex)
	}
}

func TestJoinWithOnlyOneElementDifferent(t *testing.T) {
	arr := []string{"onlyone"}
	if ajpfuzzer.Join(arr, ",") != "onlyone" {
		t.Errorf("Expected 'onlyone', got '%s'", ajpfuzzer.Join(arr, ","))
	}
}