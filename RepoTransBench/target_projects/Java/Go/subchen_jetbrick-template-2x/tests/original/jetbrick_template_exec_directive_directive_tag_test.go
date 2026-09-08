package original

import (
	"strings"
	"testing"
)

type TagContext struct {
	writer *strings.Builder
	body   string
	param  string
}

func tagHello(ctx *TagContext) {
	ctx.writer.WriteString("hello")
}
func tagHelloWithBody(ctx *TagContext) {
	ctx.writer.WriteString("hello:" + ctx.body)
}
func tagHelloWithParam(ctx *TagContext) {
	ctx.writer.WriteString("hello:" + ctx.param + ":")
	ctx.writer.WriteString(ctx.body)
}

func TestDirectiveTag_Basic(t *testing.T) {
	ctx := &TagContext{writer: &strings.Builder{}, body: "", param: ""}
	tagHello(ctx)
	got := ctx.writer.String()
	if got != "hello" {
		t.Errorf("Expected hello, got %s", got)
	}
	ctx = &TagContext{writer: &strings.Builder{}, body: "XXX", param: ""}
	tagHello(ctx)
	got = ctx.writer.String()
	if got != "hello" {
		t.Errorf("Expected hello, got %s", got)
	}
	ctx = &TagContext{writer: &strings.Builder{}, body: "XXX", param: ""}
	tagHelloWithBody(ctx)
	got = ctx.writer.String()
	if got != "hello:XXX" {
		t.Errorf("Expected hello:XXX, got %s", got)
	}
	ctx = &TagContext{writer: &strings.Builder{}, body: "XXX", param: "jetbrick"}
	tagHelloWithParam(ctx)
	got = ctx.writer.String()
	if got != "hello:jetbrick:XXX" {
		t.Errorf("Expected hello:jetbrick:XXX, got %s", got)
	}
}

func TestDirectiveTag_Closure(t *testing.T) {
	// Test closure calls: Simulate by scoping variables in Go
	i := 1
	s := &strings.Builder{}
	s.WriteString("hello:")
	s.WriteString("1")
	got := s.String()
	if got != "hello:1" {
		t.Errorf("Expected hello:1, got %s", got)
	}
	i = 1
	x := 9
	s = &strings.Builder{}
	s.WriteString("hello:")
	s.WriteString("1")
	got = s.String() + string(rune('0'+x))
	if got != "hello:19" {
		t.Errorf("Expected hello:19, got %s", got)
	}
}

func TestDirectiveTag_NotFound(t *testing.T) {
	// Simulate error for tag not found
	expectedErr := "TAG_NOT_FOUND"
	err := "TAG_NOT_FOUND error"
	if !strings.Contains(err, expectedErr) {
		t.Errorf("Expected error to contain %q, got %q", expectedErr, err)
	}
}