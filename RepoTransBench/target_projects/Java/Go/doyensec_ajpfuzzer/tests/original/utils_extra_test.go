package original

import (
	"reflect"
	"testing"

	"ajpfuzzer"
)

func TestRandomStringAllCharsEdge(t *testing.T) {
	res := ajpfuzzer.RandomString(5, "x")
	if res != "xxxxx" {
		t.Errorf("Expected 'xxxxx', got '%s'", res)
	}
}

func TestGetRandomIntMinGreaterThanMaxThrows(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for min > max")
		}
	}()
	_ = ajpfuzzer.GetRandomInt(5, 2)
}

func TestCreateMapFromPairsTypeSafety(t *testing.T) {
	m := ajpfuzzer.CreateMapFromPairs(1, "a", 2, "b")
	if m[1] != "a" {
		t.Errorf("Key 1 expected 'a', got '%v'", m[1])
	}
	if m[2] != "b" {
		t.Errorf("Key 2 expected 'b', got '%v'", m[2])
	}
}

func TestToHexUpperByteValues(t *testing.T) {
	arr := []byte{0xaf, 0xff, 0xb4}
	hex := ajpfuzzer.ToHex(arr)
	if hex != "afffb4" {
		t.Errorf("Expected 'afffb4', got '%s'", hex)
	}
}

func TestJoinWithOnlyOneElement(t *testing.T) {
	arr := []string{"solo"}
	if ajpfuzzer.Join(arr, ",") != "solo" {
		t.Errorf("Expected 'solo', got '%s'", ajpfuzzer.Join(arr, ","))
	}
}