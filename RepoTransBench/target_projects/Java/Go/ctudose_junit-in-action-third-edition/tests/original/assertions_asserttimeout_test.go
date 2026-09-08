package original

import (
	"testing"
	"time"
)

type Job struct {
	Name string
}

type SUTTimeout struct {
	systemName string
	jobs       []Job
}

func NewSUTTimeout(name string) *SUTTimeout {
	return &SUTTimeout{systemName: name}
}

func (s *SUTTimeout) AddJob(job Job) {
	s.jobs = append(s.jobs, job)
}

func (s *SUTTimeout) Run(delayMillis int) {
	time.Sleep(time.Duration(delayMillis) * time.Millisecond)
}

func TestTimeout(t *testing.T) {
	sut := NewSUTTimeout("Our system under test")
	sut.AddJob(Job{"Job 1"})
	doneCh := make(chan struct{})
	go func() {
		sut.Run(200)
		close(doneCh)
	}()
	select {
	case <-doneCh:
		// Passed
	case <-time.After(500 * time.Millisecond):
		t.Fatal("Timeout: job was not completed in time")
	}
}

func TestTimeoutPreemptively(t *testing.T) {
	sut := NewSUTTimeout("Our system under test")
	sut.AddJob(Job{"Job 1"})
	doneCh := make(chan struct{})
	go func() {
		sut.Run(200)
		close(doneCh)
	}()
	select {
	case <-doneCh:
		// Passed
	case <-time.After(500 * time.Millisecond):
		t.Fatal("Timeout preemptively: job was not completed in time")
	}
}