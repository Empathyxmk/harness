package tests

import (
	"testing"
)

type Pipe struct {
	OutFD    int
	InFD     int
	OutClosed bool
	InClosed  bool
	WritePath string
}

func (p *Pipe) CloseIn()  { p.InClosed = true }
func (p *Pipe) CloseOut() { p.OutClosed = true }

func TestPipeCreationAndClose(t *testing.T) {
	p := &Pipe{OutFD: 10, InFD: 11, WritePath: "/dev/fd/10"}
	if p.OutFD == 0 || p.InFD == 0 {
		t.Error("fds should be ints")
	}
	if p.OutClosed {
		t.Error("out not expected closed")
	}
	if p.InClosed {
		t.Error("in not expected closed")
	}
	if p.WritePath == "" {
		t.Error("no write path")
	}
	// Simulate closing fds
	p.CloseIn()
	if !p.InClosed {
		t.Error("close in failed")
	}
	p = &Pipe{}
	p.CloseOut()
	if !p.OutClosed {
		t.Error("close out failed")
	}
}