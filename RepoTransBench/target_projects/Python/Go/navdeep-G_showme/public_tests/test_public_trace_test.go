package public_tests

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
)

func Trace(args ...any) {
	txt := ""
	for _, arg := range args {
		txt += " " + toString(arg)
	}
	println(txt)
}

func toString(a any) string {
	switch v := a.(type) {
	case string:
		return v
	case int:
		return string(rune(v))
	default:
		return "<unknown>"
	}
}

func TestTraceFunctionality(t *testing.T) {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	Trace("Trace public test", 456)
	w.Close()
	os.Stdout = old

	var buf bytes.Buffer
	io.Copy(&buf, r)
	out := buf.String()
	if !strings.Contains(out, "Trace public test") {
		t.Error("Expected output to have 'Trace public test', got:", out)
	}
}