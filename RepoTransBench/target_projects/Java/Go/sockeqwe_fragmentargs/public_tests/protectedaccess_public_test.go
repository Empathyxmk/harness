package public_tests

import (
	"testing"
)

func TestProtectedFieldAccessTestPublicVariant(t *testing.T) {
	dummy := &DummyProtectedObjectPublic{}
	dummy.SetValue("barBaz")
	if got := dummy.GetValue(); got != "barBaz" {
		t.Errorf("Expected \"barBaz\", got %q", got)
	}
}

type DummyProtectedObjectPublic struct {
	Field string
}

func (d *DummyProtectedObjectPublic) SetValue(val string) {
	d.Field = val
}
func (d *DummyProtectedObjectPublic) GetValue() string {
	return d.Field
}