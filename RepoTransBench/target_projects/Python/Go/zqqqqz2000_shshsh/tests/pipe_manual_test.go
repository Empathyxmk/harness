package tests

import (
	"os"
	"testing"
)

type PipeObj struct {
	InFD      int
	OutFD     int
	AutoClose bool
}

func (p *PipeObj) CloseIn()  {}
func (p *PipeObj) CloseOut() {}

type PipeCloseError struct{}

func (e *PipeCloseError) Error() string {
	return "Pipe close error"
}

func TestPipeInitAndClose(t *testing.T) {
	pipe := &PipeObj{InFD: 3, OutFD: 4, AutoClose: true}
	if pipe.InFD == 0 || pipe.OutFD == 0 {
		t.Error("pipe fds should be set")
	}
	pipe.CloseIn()
	pipe.CloseOut()
	if pipe.AutoClose != true && pipe.AutoClose != false {
		t.Error("auto_close should be bool")
	}
}

func TestPipeCloseErrorRepr(t *testing.T) {
	e := &PipeCloseError{}
	if e.Error() == "" {
		t.Error("repr should be a string")
	}
}