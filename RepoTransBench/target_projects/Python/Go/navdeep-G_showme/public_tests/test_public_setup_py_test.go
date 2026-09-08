package public_tests

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
)

func SetupPyMain(args []string) {
	println("SetupPyMain called with", strings.Join(args, ","))
}

func TestPublicSetupMainRuns(t *testing.T) {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	SetupPyMain([]string{"--version"})
	w.Close()
	os.Stdout = old

	var buf bytes.Buffer
	io.Copy(&buf, r)
	out := buf.String()
	if !strings.Contains(out, "SetupPyMain called with") {
		t.Error("Print should have been called by SetupPyMain")
	}
}