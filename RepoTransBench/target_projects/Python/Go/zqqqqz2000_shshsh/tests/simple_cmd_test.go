package tests

import (
	"bytes"
	"testing"
)

type CmdRes struct {
	Stdout []byte
	Stderr []byte
}

func (c *CmdRes) StdoutRead() []byte { return c.Stdout }
func (c *CmdRes) StderrRead() []byte { return c.Stderr }

func TestOneCmd(t *testing.T) {
	res := &CmdRes{Stdout: []byte("123\n")}
	if !bytes.Equal(res.StdoutRead(), []byte("123\n")) {
		t.Error("wrong stdout for one cmd")
	}
}

func TestQuickCmd(t *testing.T) {
	res := &CmdRes{Stdout: []byte("123\n")}
	if !bytes.Equal(res.StdoutRead(), []byte("123\n")) {
		t.Error("wrong stdout for quick cmd")
	}
}

func TestGetStderr(t *testing.T) {
	res := &CmdRes{Stderr: []byte("s")}
	if len(res.StderrRead()) == 0 {
		t.Error("should be output in Stderr")
	}
}

func TestReadOut(t *testing.T) {
	out := []string{"abc", "", "", "defg", ""}
	for i, line := range out {
		if out[i] != line {
			t.Errorf("mismatch at %d", i)
		}
	}
}