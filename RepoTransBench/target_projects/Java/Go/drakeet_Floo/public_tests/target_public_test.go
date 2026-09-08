package public_tests

import "testing"

type Target struct {
	url        string
	targetClass string
}
func NewTarget(url, targetClass string) *Target {
	return &Target{url: url, targetClass: targetClass}
}
func (t *Target) GetUrl() string             { return t.url }
func (t *Target) GetTargetClass() string     { return t.targetClass }
func (t *Target) SetUrl(url string)          { t.url = url }

func TestCreateAndGetUrl_public(t *testing.T) {
	target := NewTarget("foo://bar", "SomeClass")
	if target.GetUrl() != "foo://bar" {
		t.Errorf("GetUrl expected 'foo://bar', got %v", target.GetUrl())
	}
	if target.GetTargetClass() != "SomeClass" {
		t.Errorf("TargetClass expected 'SomeClass', got %v", target.GetTargetClass())
	}
}

func TestSetUrl_public(t *testing.T) {
	target := NewTarget("foo://baz", "OtherClass")
	target.SetUrl("foo://changed")
	if target.GetUrl() != "foo://changed" {
		t.Errorf("expected changed url, got %v", target.GetUrl())
	}
}