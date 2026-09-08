package original

import (
	"testing"
)

type SUT struct {
	systemName string
	verified   bool
}

func NewSUTAll(name string) *SUT {
	return &SUT{systemName: name}
}
func (s *SUT) IsVerified() bool { return s.verified }
func (s *SUT) GetSystemName() string { return s.systemName }
func (s *SUT) Verify()           { s.verified = true }

func TestSystemNotVerified(t *testing.T) {
	sut := NewSUTAll("Our system under test")
	if sut.GetSystemName() != "Our system under test" {
		t.Error("Default SUT system name incorrect")
	}
	if sut.IsVerified() {
		t.Error("By default, SUT is not under current verification")
	}
}

func TestSystemUnderVerification(t *testing.T) {
	sut := NewSUTAll("Our system under test")
	sut.Verify()
	if sut.GetSystemName() != "Our system under test" {
		t.Error("SUT system name after verify still incorrect")
	}
	if !sut.IsVerified() {
		t.Error("SUT should be marked as verified after calling verify")
	}
}