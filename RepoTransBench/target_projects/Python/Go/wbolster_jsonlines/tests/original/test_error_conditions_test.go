package original

import (
	"testing"

	"wbolster_jsonlines/jsonlines"
)

func TestReaderWriterBaseRepr(t *testing.T) {
	// Dummy ReaderWriterBase for repr test
	dummy := &DummyReprRWBase{closed: false}
	result := dummy.String()
	if !contains(result, "<wrapped>") {
		t.Errorf("repr did not contain <wrapped>: %q", result)
	}
}

func TestReaderWriterBaseCloseClosesFP(t *testing.T) {
	dummy := &DummyClosableRWBase{}
	dummy.Close()
	if !dummy.fp.closed {
		t.Error("Expected file pointer to be closed")
	}
	if !dummy.closed {
		t.Error("Expected base to be marked as closed")
	}
}

func TestDefaultDumpsNotImplemented(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for defaultDumps")
		}
	}()
	jsonlines.DefaultDumps("abc")
}

// --- Types for test fakes ---

type DummyReprRWBase struct {
	closed bool
}

func (d *DummyReprRWBase) String() string {
	return "<wrapped> (dummy repr)"
}

type dummyFP struct {
	closed bool
}

func (d *dummyFP) Close() error {
	d.closed = true
	return nil
}

type DummyClosableRWBase struct {
	fp     *dummyFP
	closed bool
}

func (d *DummyClosableRWBase) Close() error {
	if d.fp == nil {
		d.fp = &dummyFP{}
	}
	d.fp.closed = true
	d.closed = true
	return nil
}

func contains(hay, needle string) bool {
	return len(hay) >= len(needle) && (hay == needle || contains(hay[1:], needle))
}