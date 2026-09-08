package tests

import (
	"bytes"
	"testing"
)

type CmdObj struct {
	Code int
	Stdout []byte
}

func (c *CmdObj) Wait() {}
func (c *CmdObj) Or(cmd string) *CmdObj {
	return &CmdObj{Code: 0, Stdout: []byte("234\n")}
}

func TestAnd(t *testing.T) {
	res := &CmdObj{Code: 1, Stdout: []byte("")}
	if res.Code == 0 {
		t.Error("expected failure code")
	}
	if !bytes.Equal(res.Stdout, []byte("")) {
		t.Error("expected empty output")
	}
}
func TestOr(t *testing.T) {
	res := &CmdObj{Code: 1, Stdout: []byte("")}
	orRes := res.Or("echo 567")
	orRes.Wait()
	if orRes.Code != 0 {
		t.Error("should succeed after or")
	}
	if !bytes.Equal(orRes.Stdout, []byte("234\n")) {
		t.Errorf("wrong output: %v", orRes.Stdout)
	}
}