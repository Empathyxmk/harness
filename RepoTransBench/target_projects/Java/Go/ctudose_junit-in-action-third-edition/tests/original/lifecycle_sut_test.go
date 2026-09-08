package original

import (
	"testing"
)

// ResourceForAllTests simulates a global resource.
type ResourceForAllTests struct {
	resourceName string
}

func NewResourceForAllTests(resourceName string) *ResourceForAllTests {
	// In Java, this prints, but we ignore output in Go tests.
	return &ResourceForAllTests{resourceName}
}
func (r *ResourceForAllTests) Close() {}

type SUT struct {
	systemName string
}

func NewSUT(name string) *SUT {
	return &SUT{systemName: name}
}
func (s *SUT) Close()         {}
func (s *SUT) CanReceiveRegularWork() bool { return true }
func (s *SUT) CanReceiveAdditionalWork() bool { return false }

func TestSUTSetupTeardown(t *testing.T) {
	// @BeforeAll and @AfterAll simulated by static variable and defer
	resource := NewResourceForAllTests("Our resource for all tests")
	defer resource.Close()
	systemUnderTest := NewSUT("Our system under test")
	defer systemUnderTest.Close()

	if !systemUnderTest.CanReceiveRegularWork() {
		t.Error("SUT should be able to receive regular work")
	}
	if systemUnderTest.CanReceiveAdditionalWork() {
		t.Error("SUT should not be able to receive additional work")
	}
}