package original

import (
	"testing"
	"errors"
)

type SUTThrows struct {
	systemName string
	jobs       []int
}

func NewSUTThrows(name string) *SUTThrows {
	return &SUTThrows{systemName: name}
}

func (s *SUTThrows) Run() error {
	return errors.New("No jobs on the execution list!")
}
func (s *SUTThrows) RunJob(job int) error {
	return errors.New("No jobs on the execution list!")
}

func TestExpectedException(t *testing.T) {
	sut := NewSUTThrows("Our system under test")
	if err := sut.Run(); err == nil {
		t.Error("Expected an error to be thrown")
	}
}

func TestCatchException(t *testing.T) {
	sut := NewSUTThrows("Our system under test")
	err := sut.RunJob(1000)
	if err == nil {
		t.Error("Expected a NoJobException error")
	}
	if err != nil && err.Error() != "No jobs on the execution list!" {
		t.Errorf("Expected 'No jobs on the execution list!', got '%s'", err.Error())
	}
}