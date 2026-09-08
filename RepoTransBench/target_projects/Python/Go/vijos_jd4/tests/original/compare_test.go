package original

import (
	"bytes"
	"testing"
)

func compareStream(a, b []byte) bool {
	return bytes.Equal(bytes.TrimSpace(a), bytes.TrimSpace(b))
}

func TestSmallCompare(t *testing.T) {
	if !compareStream([]byte(""), []byte("")) {
		t.Errorf("empty strings should compare true")
	}
	if !compareStream([]byte("a"), []byte("a")) {
		t.Errorf("a vs a should compare true")
	}
	if compareStream([]byte("a"), []byte("b")) {
		t.Errorf("a vs b should compare false")
	}
	if !compareStream([]byte("bar"), []byte("bar")) {
		t.Errorf("bar vs bar should compare true")
	}
	if compareStream([]byte("bar"), []byte("baz")) {
		t.Errorf("bar vs baz should compare false")
	}
}

func TestAPlusBCompare(t *testing.T) {
	answer := []byte("1 2\r\n")
	tests := []struct {
		input    []byte
		expected bool
	}{
		{[]byte("1 2"), true},
		{[]byte("1 2\n"), true},
		{[]byte("1 2\r"), true},
		{[]byte("1 2\r\n"), true},
		{[]byte("1 2 "), true},
		{[]byte("1 2 \n"), true},
		{[]byte("1 2 \r"), true},
		{[]byte("1 2 \r\n"), true},
		{[]byte("1  2"), true},
		{[]byte("1  2\n"), true},
		{[]byte("1  2\r"), true},
		{[]byte("1  2\r\n"), true},
		{[]byte("1  2 "), true},
		{[]byte("1  2 \n"), true},
		{[]byte("1  2 \r"), true},
		{[]byte("1  2 \r\n"), true},
		{[]byte(" 1 2"), true},
		{[]byte(" 1 2\n"), true},
		{[]byte(" 1 2\r"), true},
		{[]byte(" 1 2\r\n"), true},
		{[]byte(" 1 2 "), true},
		{[]byte(" 1 2 \n"), true},
		{[]byte(" 1 2 \r"), true},
		{[]byte(" 1 2 \r\n"), true},
		{[]byte("1 1"), false},
		{[]byte("1 1\n"), false},
		{[]byte("1 1\r"), false},
		{[]byte("1 1\r\n"), false},
		{[]byte("1 1 "), false},
		{[]byte("1 1 \n"), false},
		{[]byte("1 1 \r"), false},
		{[]byte("1 1 \r\n"), false},
		{[]byte(" 1 1"), false},
		{[]byte(" 1 1\n"), false},
		{[]byte(" 1 1\r"), false},
		{[]byte(" 1 1\r\n"), false},
		{[]byte(" 1 1 "), false},
		{[]byte(" 1 1 \n"), false},
		{[]byte(" 1 1 \r"), false},
		{[]byte(" 1 1 \r\n"), false},
		{[]byte("2 2"), false},
		{[]byte("2 2\n"), false},
		{[]byte("2 2\r"), false},
		{[]byte("2 2\r\n"), false},
		{[]byte("2 2 "), false},
		{[]byte("2 2 \n"), false},
		{[]byte("2 2 \r"), false},
		{[]byte("2 2 \r\n"), false},
		{[]byte(" 2 2"), false},
		{[]byte(" 2 2\n"), false},
		{[]byte(" 2 2\r"), false},
		{[]byte(" 2 2\r\n"), false},
		{[]byte(" 2 2 "), false},
		{[]byte(" 2 2 \n"), false},
		{[]byte(" 2 2 \r"), false},
		{[]byte(" 2 2 \r\n"), false},
		{[]byte("2 1"), false},
		{[]byte("2 1\n"), false},
		{[]byte("2 1\r"), false},
		{[]byte("2 1\r\n"), false},
		{[]byte("2 1 "), false},
		{[]byte("2 1 \n"), false},
		{[]byte("2 1 \r"), false},
		{[]byte("2 1 \r\n"), false},
		{[]byte(" 2 1"), false},
		{[]byte(" 2 1\n"), false},
		{[]byte(" 2 1\r"), false},
		{[]byte(" 2 1\r\n"), false},
		{[]byte(" 2 1 "), false},
		{[]byte(" 2 1 \n"), false},
		{[]byte(" 2 1 \r"), false},
		{[]byte(" 2 1 \r\n"), false},
		{[]byte("12"), false},
	}
	for _, test := range tests {
		got := compareStream(answer, test.input)
		if got != test.expected {
			t.Errorf("compare(%q, %q): got %v, want %v",
				answer, test.input, got, test.expected)
		}
	}
}

func TestLargeCompare(t *testing.T) {
	oneMB := bytes.Repeat([]byte("a"), 1048576)
	bMB := bytes.Repeat([]byte("b"), 1048576)
	assertTrue := func(cond bool, desc string) {
		if !cond {
			t.Errorf("Expected true: %v", desc)
		}
	}
	assertFalse := func(cond bool, desc string) {
		if cond {
			t.Errorf("Expected false: %v", desc)
		}
	}
	assertTrue(compareStream(oneMB, oneMB), "equal 1MB blocks")
	oneMB1 := append(oneMB[:1048575], 'b')
	assertFalse(compareStream(oneMB, oneMB1), "last byte changed")
	longMixA := append(append(oneMB, ' '), append(bMB, []byte("\r\n")...)...)
	longMixB := append(oneMB, append(bytes.Repeat([]byte(" "), 1048576), bMB...)...)
	assertTrue(compareStream(longMixA, longMixB), "giant equivalency")
}