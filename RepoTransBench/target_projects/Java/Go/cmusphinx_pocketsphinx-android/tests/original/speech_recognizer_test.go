package original

import (
	"testing"
)

// Minimal dummy Implementation for test logic
type Hypothesis struct {
	Hypstr    string
	BestScore int
}

type RecognitionListener interface {
	OnReadyForSpeech()
	OnBeginningOfSpeech()
	OnEndOfSpeech()
	OnPartialResult(hypothesis *Hypothesis)
	OnResult(hypothesis *Hypothesis)
	OnError(err error)
	OnTimeout()
}

type dummyListener struct {
	ready bool
}
func (d *dummyListener) OnReadyForSpeech()                { d.ready = true }
func (d *dummyListener) OnBeginningOfSpeech()             {}
func (d *dummyListener) OnEndOfSpeech()                   {}
func (d *dummyListener) OnPartialResult(_ *Hypothesis)    {}
func (d *dummyListener) OnResult(_ *Hypothesis)           {}
func (d *dummyListener) OnError(_ error)                  {}
func (d *dummyListener) OnTimeout()                       {}

type SpeechRecognizer struct{
	listeners []RecognitionListener
}

func NewSpeechRecognizer() *SpeechRecognizer {
	return &SpeechRecognizer{}
}

func (s *SpeechRecognizer) AddListener(l RecognitionListener) {
	s.listeners = append(s.listeners, l)
}
func (s *SpeechRecognizer) RemoveListener(l RecognitionListener) {
	// Remove by identity - in real code, compare pointers
	newListeners := s.listeners[:0]
	for _, ll := range s.listeners {
		if ll != l {
			newListeners = append(newListeners, ll)
		}
	}
	s.listeners = newListeners
}
func (s *SpeechRecognizer) StartListening(search string) {
	for _, l := range s.listeners {
		l.OnReadyForSpeech()
	}
}
func (s *SpeechRecognizer) Stop()   {}
func (s *SpeechRecognizer) Cancel() {}

func TestSpeechRecognizerAddAndRemoveListener(t *testing.T) {
	r := NewSpeechRecognizer()
	l := &dummyListener{}
	r.AddListener(l)
	r.RemoveListener(l)
	// should not panic (no output on success)
}

func TestSpeechRecognizerStartListeningFiresReady(t *testing.T) {
	r := NewSpeechRecognizer()
	l := &dummyListener{}
	r.AddListener(l)
	r.StartListening("search")
	if !l.ready {
		t.Errorf("Expected DummyListener.ready = true")
	}
}

func TestSpeechRecognizerStopAndCancelNoErrors(t *testing.T) {
	r := NewSpeechRecognizer()
	r.Stop()
	r.Cancel()
	// nothing to assert, just coverage
}