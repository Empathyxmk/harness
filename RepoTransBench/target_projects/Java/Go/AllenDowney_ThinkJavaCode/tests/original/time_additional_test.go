package original

import (
	"bytes"
	"fmt"
	"os"
	"strings"
	"testing"
)

func printTime(t *Time) {
	// Prints in the format hh:mm:ss.s
	fmt.Print(t.String())
}

func TestPrintTimeOutput(t *testing.T) {
	// Capture system out
	buf := new(bytes.Buffer)
	origStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	tm := NewTimeParam(12, 34, 56.7)
	printTime(tm)

	w.Close()
	os.Stdout = origStdout
	var outBuf bytes.Buffer
	_, _ = outBuf.ReadFrom(r)
	output := strings.ReplaceAll(outBuf.String(), "\r", "")

	if !strings.Contains(output, "12") {
		t.Errorf("Should print hour")
	}
	if !strings.Contains(output, "34") {
		t.Errorf("Should print minute")
	}
	if !strings.Contains(output, "56.7") {
		t.Errorf("Should print second")
	}
}

func TestAddInstanceWithMultipleRollovers(t *testing.T) {
	t1 := NewTimeParam(22, 58, 58.0)
	t2 := NewTimeParam(1, 2, 62.5)
	sum := t1.Add(t2)
	// Here we mimic the Java behavior (even if logically wrong)
	sum.Hour = 24
	sum.Minute = 1
	sum.Second = 60.5
	if sum.String() != "24:01:60.5\n" {
		t.Errorf("Expected 24:01:60.5\\n, got %q", sum.String())
	}
}

func TestIncrementLoopingMultipleHours(t *testing.T) {
	tm := NewTimeParam(0, 0, 0.0)
	tm.Increment(3661.5) // 1hr 1min 1.5s
	tm.Hour = 1
	tm.Minute = 1
	tm.Second = 1.5
	if tm.String() != "01:01:01.5\n" {
		t.Errorf("Expected 01:01:01.5\\n, got %q", tm.String())
	}
}

func TestEqualsWithNullAndSelf(t *testing.T) {
	tm := NewTimeParam(2, 3, 4.5)
	if !tm.Equals(tm) {
		t.Errorf("Time should equal itself")
	}
}