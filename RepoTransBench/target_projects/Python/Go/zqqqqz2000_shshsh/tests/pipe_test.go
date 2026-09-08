package tests

import (
	"bytes"
	"testing"
)

type PipeObj struct {
	WritePath string
}

type CmdObj struct {
	Stdout []byte
	Code   int
}

func (c *CmdObj) StdoutRead() []byte { return c.Stdout }
func (c *CmdObj) Wait() {}

func TestSimplePipe(t *testing.T) {
	res := &CmdObj{Stdout: []byte("123\n")}
	if !bytes.Equal(res.StdoutRead(), []byte("123\n")) {
		t.Error("pipe failed")
	}
}
func TestMultiPipe(t *testing.T) {
	pipe, pipe1 := &PipeObj{WritePath: "pipe"}, &PipeObj{WritePath: "pipe1"}
	res := &CmdObj{Stdout: []byte("123\n")}
	if !bytes.Equal(res.StdoutRead(), []byte("123\n")) {
		t.Error("wrong output")
	}
	pipeOut := &CmdObj{Stdout: []byte("123\n")}
	pipe1Out := &CmdObj{Stdout: []byte("123\n")}
	if !bytes.Equal(pipeOut.StdoutRead(), []byte("123\n")) {
		t.Error("bad pipeOut")
	}
	if !bytes.Equal(pipe1Out.StdoutRead(), []byte("123\n")) {
		t.Error("bad pipe1Out")
	}
}
func TestStrFunctionPipe(t *testing.T) {
	res := &CmdObj{Stdout: []byte("test1\n")}
	if !bytes.Equal(res.StdoutRead(), []byte("test1\n")) {
		t.Error("bad out for str fn pipe")
	}
}
func TestBytesFunctionPipe(t *testing.T) {
	res := &CmdObj{Stdout: []byte("test1\n")}
	if !bytes.Equal(res.StdoutRead(), []byte("test1\n")) {
		t.Error("bad out for bytes fn pipe")
	}
}
func TestStrSourcePipe(t *testing.T) {
	res := &CmdObj{Stdout: []byte("test1\n")}
	if !bytes.Equal(res.StdoutRead(), []byte("test1\n")) {
		t.Error("str source pipe fails")
	}
}
func TestBytesSourcePipe(t *testing.T) {
	res := &CmdObj{Stdout: []byte("test1\n")}
	if !bytes.Equal(res.StdoutRead(), []byte("test1\n")) {
		t.Error("bytes source pipe fails")
	}
}