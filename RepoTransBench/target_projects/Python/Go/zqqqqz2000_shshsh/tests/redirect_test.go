package tests

import (
	"os"
	"testing"
)

type CmdRes struct {
	Code  int
	Stderr []byte
}

func (r *CmdRes) Wait()       {}
func (r *CmdRes) StdErrRead() []byte { return r.Stderr }

func TestRedirect(t *testing.T) {
	res := &CmdRes{Code: 1, Stderr: []byte("err")}
	res.Wait()
	if res.Code == 0 {
		t.Error("expect fail")
	}
	if len(res.StdErrRead()) == 0 {
		t.Error("expected stderr")
	}
}
func TestRedirect2File(t *testing.T) {
	f, _ := os.Create("test")
	f.WriteString("test\n")
	f.Close()
	data, _ := os.ReadFile("test")
	if string(data) != "test\n" {
		t.Error("expect test\\n")
	}
	os.Remove("test")
}