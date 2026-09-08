package tests

import (
	"bytes"
	"errors"
	"testing"
)

// Import your library shshsh here, e.g., "zqqqqz2000_shshsh/shshsh"

func TestParse(t *testing.T) {
	res := Sh("echo #{}").Percent("test")
	out := res.StdoutRead()
	if !bytes.Equal(out, []byte("test\n")) {
		t.Errorf("expected b\"test\\n\", got %v", out)
	}
}

func TestParseNamed(t *testing.T) {
	res := Sh("echo #{name}").Percent(map[string]interface{}{"name": "test"})
	out := res.StdoutRead()
	if !bytes.Equal(out, []byte("test\n")) {
		t.Errorf("expected b\"test\\n\", got %v", out)
	}
}

func TestParseMix(t *testing.T) {
	first := Sh("echo #{name},#{},#{},#{}")
	step1 := first.Percent(map[string]interface{}{"name": "test"})
	step2 := step1.Percent("test1")
	res := step2.Percent([]interface{}{"test2", "test3"})
	out := res.StdoutRead()
	if !bytes.Equal(out, []byte("test,test1,test2,test3\n")) {
		t.Errorf("expected b\"test,test1,test2,test3\\n\", got %v", out)
	}
}

func TestParseInline(t *testing.T) {
	out := Sh("echo #{name},#{},#{},#{}").Call("test1", "test2", "test3", map[string]interface{}{"name": "test"}).StdoutRead()
	if !bytes.Equal(out, []byte("test,test1,test2,test3\n")) {
		t.Errorf("expected b\"test,test1,test2,test3\\n\", got %v", out)
	}
}

func TestMissArgument(t *testing.T) {
	res := Sh("echo #{name},#{},#{},#{}").Call("test1", "test2", "test3")
	err := res.Run()
	if err == nil {
		t.Error("expected error, but got none")
	}
}

func TestSpecFilename(t *testing.T) {
	res := I.RShift("cat tests/case1/spec_[token]")
	out := res.StdoutRead()
	if !bytes.Equal(out, []byte("content")) {
		t.Errorf("expected b\"content\", got %v", out)
	}
}